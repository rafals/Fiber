from stream import start, Redirect, Avoid
from views import mako

# próba stworzenia obiektowych kontrollerów - słabe rozwiązanie

class BasicController(object):
  def index(self, name = 'world'):
    return "hello %s" % name
  
  def __call__(self, get, post):
    get('/')(self.index)

class FormController(BasicController):
  
  def __init__(self):
    self.nick = 'guest'
  
  def index(self):
    return BasicController.index(self, self.nick)
  
  def get_form(self):
    return "render form"
  
  def post_form(self, nick = '', **kwargs):
    self.nick = nick
    return self.index()
  
  def __call__(self, get, post):
    BasicController.__call__(self, get, post)
    get('/form')(get_form)
    post('/form')(post_form)

start(FormController()) # odpalamy stronke