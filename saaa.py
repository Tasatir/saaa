"""
Proyecto SA^3
Autor: 	Mario Lopez
        Luis Aviles
		Joaquin V
Fecha: Octubre del 2012
versión: 1
"""

#Manejo de temlates en el HTML
import jinja2                    
from jinja2 import Environment, meta

import os
import cgi
import datetime
import urllib
# for hashing
import hashlib
import modelo.Layer
#Framework de Web para Python
import webapp2
                                  
# API DataStore
from google.appengine.ext import db

# intitalization of template system. It says that HTML templates will
# be found in current directory ("__file__")
jinja_environment = jinja2.Environment( \
   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# variable env para sesiones
env = Environment()

# Método para verificar si hay una sesión activa
def before_filter(fn):
	def inner_function(self):
		if not 'session' in env.globals:
			self.redirect('/')
		return fn(self)
	return inner_function

"""
REQUEST HANDLERS
"""

class MainPage(webapp2.RequestHandler):
    """Pantalla inicial. Despliega una forma para iniciar sesión
    """
            
    def get(self):

        self.response.headers['Content-Type'] = 'text/html'
        
        #productos = db.GqlQuery("SELECT * FROM Inventario")
        
        #Desplegar lista de productos
        _despliegaLogin(self, '/vistas/login.html')
			

class VerUsuarios(webapp2.RequestHandler):
	""" Despliega los usuarios registrados
	"""
	
	@before_filter
	def get(self):
		
		self.response.headers['Content-Type'] = 'text/html'
		
		#self.response.out.write( env.globals['session'])
		
		# Generar el admin
		nombre = 'admin'
		user = 'admin'
		password = 'admin'
		tipo = 'admin'
		# Generar password
		h =  hashlib.new('ripemd160')
		h.update(password)
		md5 = h.hexdigest()
		password = md5
		#Usuario(nombre = nombre, user = user, password = password, tipo = tipo).put()
		
		usuarios = db.GqlQuery("SELECT * FROM Usuario")
		
		_despliegaVerUsuarios(self, usuarios, '/vistas/verUsuarios.html')

class RegistroAlumno(webapp2.RequestHandler):
	""" Formulario para registrar usuarios
	"""
	
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		clinicas = db.GqlQuery("SELECT * FROM Clinica")
		
		_despliegaRegistroAlumno(self, clinicas, '/vistas/registroAlumno.html')

class GrabaAlumno(webapp2.RequestHandler):
	
	def post(self):
		nombre = self.request.get('nombre')
		matricula = self.request.get('matricula')
		password = self.request.get('password')
		
		# Generar password
		h =  hashlib.new('ripemd160')
		h.update(password)
		md5 = h.hexdigest()
		
		password = md5
            

class IniciaSesion(webapp2.RequestHandler):
	""" Entrada: al dar click en iniciar sesión en la pantalla principal
		Salida: se crea la sesión del usuario y lo redirige a....
	"""
	
	def post(self):		
		self.response.headers['Content-Type'] = 'text/html'
		user = self.request.get('user')
		password = self.request.get('password')
		
		h =  hashlib.new('ripemd160')
		h.update(password)
		md5 = h.hexdigest()
		password = md5
		
		user = db.GqlQuery("SELECT * FROM Usuario WHERE user = '" + user + "' AND password = '" + password + "'")
		
		if user.count() == 1:
			for u in user:
				#self.response.out.write( u.user + ' ' + u.password)
				user = []
				user.append(u.user)
				user.append(u.tipo)
				env.globals['session'] = user
				self.redirect('/bienvenida')
		else:
			self.redirect('/')

class Bienvenida(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		_despliegaBienvenida(self, '/vistas/bienvenida.html')

class AgregarClinica(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		_despliegaAgregarClinica(self, '/vistas/agregarClinica.html')

class GrabaClinica(webapp2.RequestHandler):
	def post(self):
		nombre = self.request.get('nombre')
		
		Clinica(nombre = nombre).put()
		self.redirect('/verClinicas') #redirección a listar pacientes
		

class VerClinicas(webapp2.RequestHandler):
	
	@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		clinicas = db.GqlQuery("SELECT * FROM Clinica")
		
		_despliegaVerClinicas(self, clinicas, '/vistas/verClinicas.html')
		

"""
Views
"""

def _despliegaLogin(self, templateFile):
        template = jinja_environment.get_template(templateFile)
        self.response.out.write(template.render({}))

def _despliegaVerUsuarios(self, usuarios, templateFile):
		template = jinja_environment.get_template(templateFile)
		self.response.out.write(template.render({'usuarios': usuarios }))
        
def _despliegaBienvenida(self, templateFile):
		template = jinja_environment.get_template(templateFile)
		self.response.out.write(template.render({}))
		
def _despliegaRegistroAlumno(self, clinicas, templateFile):
		template = jinja_environment.get_template(templateFile)
		self.response.out.write(template.render({'clinicas': clinicas }))

def _despliegaAgregarClinica(self, templateFile):
		template = jinja_environment.get_template(templateFile)
		self.response.out.write(template.render({}))

def _despliegaVerClinicas(self, clinicas, templateFile):
		template = jinja_environment.get_template(templateFile)
		self.response.out.write(template.render({'clinicas': clinicas }))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/iniciaSesion', IniciaSesion),
                               ('/bienvenida', Bienvenida),
                               ('/verUsuarios', VerUsuarios),
                               ('/registroAlumno', RegistroAlumno),
                               ('/grabaAlumno', GrabaAlumno),
                               ('/verClinicas', VerClinicas),
                               ('/agregarClinica', AgregarClinica),
                               ('/grabaClinica', GrabaClinica)], debug=True)
