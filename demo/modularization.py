from stream import start, Redirect, Avoid, NONE
from views import mako

## prosty controller

def hello_controller(GET, POST):
  
  @GET('/')
  def hello():
    return 'hello world'


## uruchamianie controllera

start(hello_controller)


## przypisywanie routów do istniejących funkcji

def hello(name = 'world'):
  return 'hello %s' % name

def hello_controller(GET, POST):
  
  GET('/hello/{name}')(hello)


## delegowanie do innych akcji

def hello_controller(GET, POST):
  
  @GET('/')
  def hello(name = 'world'):
    return 'hello %s' % name
  
  @GET('/hello/{name}')
  def hello_name(name): return hello(name)


## przypisywanie kilku routów do jednej akcji

def hello_controller(GET, POST):
  
  @GET('/')
  @GET('/hello/{name}')
  def hello(name = 'world'):
    return 'hello %s' % name


## delegowanie zapytania do innych controllerów

def hello2_controller(GET, POST):
  hello_controller(GET, POST)


## udostępnianie akcji controllera innym controllerom

def hello_controller(GET, POST):
  
  @GET('/hello/{name}')
  def hello(name = 'world'):
    return 'hello %s' % name
  
  return hello


## wykorzystanie akcji z innego kontrollera

def main_controller(GET, POST):
  hello = hello_controller(GET, POST)
  
  GET('/')(hello)


## wykorzystanie akcji cudzego kontrolera bez delegowania do niego requesta

def main_controller(GET, POST):
  hello = hello_controller(NONE, NONE)
  
  GET('/nick/{name}')(hello)
  
  