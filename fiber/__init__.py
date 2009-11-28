#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext.webapp.util import run_wsgi_app
from webob import Request, Response, exc
from django.utils import simplejson
import re

class Avoid(Exception):
  pass
  
class Redirect(Exception):
  def __init__(self, url):
    self.url = url

def NONE(template):
  """Zaślepka dla GET lub POST, która nie robi nic (gdy dany request przypada na drugą z tych metod)"""
  def action_getter(action):
    return action
  return action_getter

def start(controller):
  
  def fiber(environ, start_response):
    """aplikacja wsgi, która uruchamia controller"""
    
    req = Request(environ)
    
    results = [] # kolejno ułożone pasujące do requesta odpowiedzi
    
    var_regex = re.compile(r'\{(\w+)(?::([^}]+))?\}', re.VERBOSE)
    
    def methods():
      """Zwraca funkcje-dekoratory (GET, POST)"""
      
      def match_template(template):
        """sprawdza czy template pasuje do aktualnego url-a"""
        def template_to_regex(template):
          """Przerabia /ple/ple/{id} na regex"""
          regex = ''
          last_pos = 0
          for match in var_regex.finditer(template):
            regex += re.escape(template[last_pos:match.start()])
            var_name = match.group(1)
            expr = match.group(2) or '[^/]+'
            expr = '(?P<%s>%s)' % (var_name, expr)
            regex += expr
            last_pos = match.end()
          regex += re.escape(template[last_pos:])
          regex = '^%s$' % regex
          return regex
      
        return re.match(template_to_regex(template), req.path_info, re.I)
    
      def method(template, request=False, response=False, json=False):
        """GET lub POST odpalający akcję i wyrzucający wyjątek Action jeśli ma ona podpięty template pasujący do url-a"""
        def action_getter(action):
          url_match = match_template(template)
          if url_match:
            
            def act():
              resp = Response(body='')
              params = url_match.groupdict()
              if req.method == 'POST':
                params.update(dict(req.POST.items()))
              if request:
                key = request if isinstance(request, str) else 'request'
                params.update({key: req})
              if response:
                key = response if isinstance(response, str) else 'response'
                params.update({key: resp})
              body = action(**params)
              if isinstance(body, tuple):
                resp.status_int = body[1]
                body = body[0]
              if json:
                resp.content_type = json if isinstance(json, str) else 'application/json' # http://www.ietf.org/rfc/rfc4627.txt
                body = simplejson.dumps(body)
              resp.body = body
              return resp
            
            results.append(act) # dodajemy do kolejki funkcję zwracającą odpowiedź
            
          return action
        return action_getter
    
      if req.method == 'GET':
        return method, NONE
      elif req.method == 'POST':
        return NONE, method
      else:
        return NONE, NONE # sorx, brak obsługi innych metod
    
    GET, POST = methods()
    
    controller(GET, POST) # pobieramy rezultaty do tablicy results
    
    results.append(exc.HTTPNotFound) # dodajemy na końcu kolejki rezultatów 404
    
    for result in results:
      try:
        response = result()
        return response(environ, start_response) # jak daje radę to zwracamy odpowiedź
      except Redirect, r:
        return exc.HTTPMovedPermanently(location=r.url)(environ, start_response) # jak trzeba redirectować, redirectujemy
      except Avoid:
        continue # jeśli akcja wyrzuca Avoid, to ją omijany i lecimy dalej
        
  run_wsgi_app(fiber) # uruchomienie przez wsgi