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
from jinja2 import Environment, PackageLoader

import os
import cgi
import datetime
import urllib
# for hashing
import hashlib
#Layer de comunicacion con Modelo
from modelo.Layer import *
#Framework de Web para Python
import webapp2
                                  
# API DataStore
from google.appengine.ext import db

# intitalization of template system. It says that HTML templates will
# be found in current directory ("__file__")
# variable env para sesiones
env = Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

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
        
        # Generar el admin
        matricula = 'admin'
        password = 'admin'
        nombre = 'admin'
        apellidop = 'admin'
        apellidom = 'admin'
        tipo = 'admin'
        # Generar password
        h =  hashlib.new('ripemd160')
        h.update(password)
        md5 = h.hexdigest()
        password = md5

        #Usuario(matricula = matricula, password = password, nombre = nombre, apellidop = apellidop, apellidom = apellidom, tipo = tipo).put()
        
        #productos = db.GqlQuery("SELECT * FROM Inventario")
        
        #Desplegar lista de productos
        _despliegaLogin(self, '/vistas/login.html')
			

class VerUsuarios(webapp2.RequestHandler):
	""" Despliega los usuarios registrados
	"""
	
	#@before_filter
	def get(self):
		
		self.response.headers['Content-Type'] = 'text/html'
				
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

class RegistraUsuario(webapp2.RequestHandler):
	""" Formulario para registrar usuarios
	"""
	
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
				
		_despliegaRegistraUsuario(self, '/vistas/registraUsuario.html')

class GrabaUsuario(webapp2.RequestHandler):
	
	def post(self):
		nombre = self.request.get('nombre')
		matricula = self.request.get('matricula')
		password = self.request.get('password')
		apellidop = self.request.get('apellidop')
		apellidom = self.request.get('apellidom')
		tipo = self.request.get('tipo')
		
		# Generar password
		h =  hashlib.new('ripemd160')
		h.update(password)
		md5 = h.hexdigest()
		
		password = md5
		
		grabaUsuario(matricula,password,nombre,apellidop,apellidop,tipo)

class IniciaSesion(webapp2.RequestHandler):
	""" Entrada: al dar click en iniciar sesión en la pantalla principal
		Salida: se crea la sesión del usuario y lo redirige a....
	"""
	
	def post(self):		
		self.response.headers['Content-Type'] = 'text/html'
		matricula = self.request.get('matricula')
		password = self.request.get('password')
		
		h =  hashlib.new('ripemd160')
		h.update(password)
		md5 = h.hexdigest()
		password = md5
		
		user = db.GqlQuery("SELECT * FROM Usuario WHERE matricula = '" + matricula + "' AND password = '" + password + "'")
		
		if user.count() == 1:
			for u in user:
				user = []
				user.append(u.nombre)
				user.append(u.matricula)
				user.append(u.tipo)
				env.globals['session'] = user
				self.redirect('/bienvenida')
		else:
			self.redirect('/')

class CerrarSesion(webapp2.RequestHandler):
	""" Entrada: al dar click en cerrar sesión
		Salida: se elimina la sesión actual y se
		redirige a la pantalla para iniciar sesión
	"""
	
	def get(self):
		del env.globals['session']
		self.redirect('/')

class Bienvenida(webapp2.RequestHandler):
	"""	Pantalla que se muestra al iniciar sesion
	"""
	
	@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		_despliegaBienvenida(self, '/vistas/bienvenida.html')

class AgregarClinica(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		_despliegaAgregarClinica(self, '/vistas/agregarClinica.html')

class AgregaHorarioClinica(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		clinicas = getAllClinicas()
		_despliegaAgregaHorarioClinica(self,clinicas, '/vistas/agregarHorarioClinica.html')


class AgregarHorario(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		clinica = self.request.get('clinica')
		_despliegaAgregarHorario(self,clinica, '/vistas/agregarHorario.html')

class MostrarHorariosClinica(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		clinica = self.request.get('key')
		horarios = verHorarios(clinica)
		_despliegaMostrarHorariosClinica(self,horarios,clinica, '/vistas/mostrarHorariosClinica.html')

class GrabaClinica(webapp2.RequestHandler):
	def post(self):
		nombre = self.request.get('nombre')
		grabaClinica(nombre)
		self.redirect('/verClinicas') #redirección a listar pacientes

class GrabaHorario(webapp2.RequestHandler):
	def post(self):
		clinica = self.request.get('clinica')
		horaInicio = self.request.get('horaInicio')
		horaFin = self.request.get('horaFin')
		dia = self.request.get('dia')
		descripcion = self.request.get('descripcion')
		setHorario(clinica,horaInicio,horaFin,dia,descripcion)
		self.redirect('/mostrarHorariosClinica?key='+clinica) #redirección ver horarios de clinica

class EliminaHorario(webapp2.RequestHandler):
	def get(self):
		horarioKey = self.request.get('key')
        	deleteHorario(horarioKey)
        	self.redirect('/mostrarHorariosClinica?key='+self.request.get('clinica')) #redirección ver horarios de clinica


class registraCita(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		_despliegaRegistraCita(self, '/vistas/registraCita.html')	

class VerClinicas(webapp2.RequestHandler):
	#@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		clinicas = getAllClinicas()
		_despliegaVerClinicas(self, clinicas, '/vistas/verClinicas.html')

class EliminaUsuario(webapp2.RequestHandler):
	def get(self):
		usuarioKey = self.request.get('key')
		deleteUsuario(usuarioKey)
		self.redirect('/verUsuarios')

class EditaUsuario(webapp2.RequestHandler):
	def get(self):
		usuarioKey = self.request.get('key')
		usuario = getUsuario(usuarioKey);
		_despliegaEditaUsuario(self, usuario, '/vistas/editaUsuario.html')

class GuardaCambiosUsuario(webapp2.RequestHandler):
	def post(self):
		usuarioKey = self.request.get('key')
		usuario = getUsuario(usuarioKey);
		nombre = self.request.get('nombre')
		matricula = self.request.get('matricula')
		apellidop = self.request.get('apellidop')
		apellidom = self.request.get('apellidom')
		tipo = self.request.get('tipo')
		
		actualizaUsuario(usuario,nombre,matricula,apellidop,apellidom,tipo)
		self.redirect('/verUsuarios')

"""
Views
"""

def _despliegaLogin(self, templateFile):
        template = env.get_template(templateFile)
        self.response.out.write(template.render({}))

def _despliegaRegistraCita(self, templateFile):
        template = env.get_template(templateFile)
        self.response.out.write(template.render({}))

def _despliegaVerUsuarios(self, usuarios, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'usuarios': usuarios }))
        
def _despliegaBienvenida(self, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({}))
		
def _despliegaRegistroAlumno(self, clinicas, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'clinicas': clinicas }))
		
def _despliegaRegistraUsuario(self, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({}))

def _despliegaAgregaHorarioClinica(self, clinicas, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'clinicas': clinicas }))

def _despliegaMostrarHorariosClinica(self, horarios,clinica, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'horarios': horarios,'clinica':clinica }))

def _despliegaAgregarClinica(self, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({}))

def _despliegaAgregarHorario(self,clinica, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'clinica':clinica}))

def _despliegaVerClinicas(self, clinicas, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'clinicas': clinicas }))
		
def _despliegaEditaUsuario(self, usuario, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'usuario': usuario }))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/iniciaSesion', IniciaSesion),
                               ('/bienvenida', Bienvenida),
                               ('/verUsuarios', VerUsuarios),
                               ('/registroAlumno', RegistroAlumno),
                               ('/grabaAlumno', GrabaAlumno),
                               ('/registraUsuario', RegistraUsuario),
                               ('/grabaUsuario', GrabaUsuario),
                               ('/verClinicas', VerClinicas),
                               ('/agregarClinica', AgregarClinica),
                               ('/agregaHorarioClinica', AgregaHorarioClinica),
                               ('/agregarHorario', AgregarHorario),
                               ('/grabaHorario', GrabaHorario),
                               ('/mostrarHorariosClinica', MostrarHorariosClinica),
                               ('/grabaClinica', GrabaClinica),
                               ('/registraCita', registraCita),
                               ('/eliminarHorario', EliminaHorario),
                               ('/grabaClinica', GrabaClinica),
                               ('/eliminarHorario', EliminaHorario),
                               ('/cerrarSesion', CerrarSesion),
                               ('/grabaClinica', GrabaClinica),
                               ('/eliminaUsuario', EliminaUsuario),
                               ('/editaUsuario', EditaUsuario),
                               ('/guardaCambiosUsuario', GuardaCambiosUsuario)], debug=True)
