from stream import start, Redirect, Avoid
from views import mako

def demo_controller(GET, POST):
  
  @GET('/')
  def index(name = 'world'):
    return 'hello %s' % name
  
  @GET('/hello/{name}')
  def hello(name):
    return index(name) # delegujemy do innej akcji
  
  @GET('/dashboard')
  @GET('/dashboard/page/{page}')
  def dashboard(page = 1):
    """2 routy przypisane do jednej akcji"""
    return "dashboard na stronie %s" % str(page)
  
  GET('/index')(index) # przypisanie routa do istniejącej już akcji
  
  @GET('/form')
  def form():
    return """
    <form method='POST'>
      <input type='text' name='nick'/>
      <input type='submit'/>
    </form>
    """
  
  @POST('/form')
  def form_resolver(nick = '', **kwargs):
    """parametry przekazane postem lądują w argumentach słownikowych
    należy przechwytywać **kwargs, aby ktoś wysyłając postem inne parametry nie wywołał TypeError'a"""
    return index(nick) # delegujemy do innej akcji
  
  
  @GET('/redirect')
  def redir():
    raise Redirect('/')
  
  @GET('/avoid')
  def avoid1():
    """przejście do kolejnej pasującej akcji"""
    raise Avoid()
  
  @GET('/avoid')
  def avoid2():
    return 'ta strona jest wyświetlana pod url /avoid'
  
  @GET('/404')
  def status():
    return 'ta strona nie istnieje', 404
  
  @GET('/json', json=True)
  def json():
    """daje application/json content type i zamienia podaną strukturę pythona na json"""
    return {'a': 'b', 'tab': [1,2,3]}
  
  @GET('/mako')
  def mako_test():
    """renderuje views/template_name.mako z podanymi parametrami"""
    return mako('template_name', param1='val1', param2='val2')
  
  @GET('/browser', request=True)
  def browser(request):
    """prosi o obiekt request, który dostaje w argumencie"""
    return request.user_agent
  
  @GET('/plain_text', response=True)
  def plain_text(response):
    response.content_type = 'text'
    return 'plain text'

start(demo_controller) # odpalamy stronke