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

class AgregaHorarioClinica(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		clinicas = getAllClinicas()
		_despliegaAgregaHorarioClinica(self,clinicas, '/vistas/agregarHorarioClinica.html')


#=======================================Funciones de Clinica
class AgregarClinica(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		_despliegaAgregarClinica(self, '/vistas/Clinica/agregarClinica.html')

class GrabaClinica(webapp2.RequestHandler):
	def post(self):
		key = self.request.get('key')
		nombre = self.request.get('nombre')
		descripcion = self.request.get('descripcion')
		localizacion = self.request.get('localizacion')
		unidades = int(self.request.get('unidades'))
		defectuosas = int(self.request.get('defectuosas'))
		if(key == None or key ==""):
			grabaClinica(nombre,descripcion,localizacion,unidades,defectuosas)
		else:
			actualizaClinica(key,nombre,descripcion,localizacion,unidades,defectuosas)
		self.redirect('/verClinicas') #Redireccion a la vista de clinicas

class EliminaClinica(webapp2.RequestHandler):
	def get(self):
		key = self.request.get('key')
		eliminaClinica(key)
		self.redirect('/verClinicas') #Redireccion a las clinicas

class VerClinicas(webapp2.RequestHandler):
	#@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		clinicas = getAllClinicas()
		_despliegaVerClinicas(self, clinicas, '/vistas/Clinica/verClinicas.html')

class EditaClinica(webapp2.RequestHandler):
	#@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		clinica = db.get(self.request.get('key'))
		_despliegaEditaClinica(self, clinica, '/vistas/Clinica/editaClinica.html')

#=======================================Fin de manejos de Clinicas
#=======================================Inicia Manejo de Grupos
class AgregarGrupo(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		_despliegaAgregarGrupo(self,self.request.get('key'), '/vistas/Grupo/agregarGrupo.html')

class GrabarGrupo(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		key = self.request.get('key')
		clinica = self.request.get('clinica')
		nombre = self.request.get('nombre')
		descripcion = self.request.get('descripcion')
		if(key == None or  key == ""):
			grabaGrupo(clinica,nombre,descripcion)
		else:
			actualizaGrupo(key,nombre,descripcion)
		self.redirect('/verGrupos?key='+clinica) #Redireccion a la vista de Grupos de una Clinica

class EliminarGrupo(webapp2.RequestHandler):
	def get(self):
		key = self.request.get('key')
		eliminaGrupo(key)
		self.redirect('/verGrupos?key='+self.request.get('clinica')) #Redireccion a la vista de los Grupos

class VerGrupos(webapp2.RequestHandler):
	#@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		grupos = getAllGrupos(self.request.get('key'))
		clinica = getObject(self.request.get('key'))
		_despliegaVerGrupos(self,clinica, grupos, '/vistas/Grupo/verGrupos.html')

class EditarGrupo(webapp2.RequestHandler):
	#@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		grupo = db.get(self.request.get('key'))
		clinica = self.request.get('clinica')
		_despliegaEditaGrupo(self, clinica, grupo, '/vistas/Grupo/editaGrupo.html')

#=======================================Fin de manejo de Grupos
#=======================================Inicia Manejo de Horarios
class AgregarHorario(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		_despliegaAgregarHorario(self,self.request.get('key'), '/vistas/Horario/agregarHorario.html')

class GrabarHorario(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		key = self.request.get('key')
		grupo = self.request.get('grupo')
		descripcion = self.request.get('descripcion')
		dia = self.request.get('dia')
		horaInicio = self.request.get('horaInicio')
		horaFin = self.request.get('horaFin')
		if(key == None or  key == ""):
			grabaHorario(grupo,descripcion,dia,horaInicio,horaFin)
		else:
			actualizaGrupo(key,descripcion,dia,horaInicio,horaFin)
		self.redirect('/verHorarios?key='+grupo) #Redireccion a la vista de Grupos de una Clinica

class EliminarHorario(webapp2.RequestHandler):
	def get(self):
		key = self.request.get('key')
		eliminaHorario(key)
		self.redirect('/verHorarios?key='+self.request.get('grupo')) #Redireccion a la vista de Horarios

class VerHorarios(webapp2.RequestHandler):
	#@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		#horarios = getAllHorarios(self.request.get('key'))
		grupo = getObject(self.request.get('key'))
		_despliegaVerHorarios(self,grupo, grupo.horarios, '/vistas/Horario/verHorarios.html')

class EditarHorario(webapp2.RequestHandler):
	#@before_filter
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		horario = db.get(self.request.get('key'))
		grupo = self.request.get('grupo')
		_despliegaEditaHorario(self, grupo, horario, '/vistas/Horario/editaHorario.html')

#=======================================Fin de manejo de Horario

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

"""
Despliega la vista para agregar un grupo nuevo
"""
def _despliegaAgregarGrupo(self,clinica, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'clinica':clinica}))
def _despliegaAgregarHorario(self,grupo, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'grupo':grupo}))
def _despliegaVerClinicas(self, clinicas, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'clinicas': clinicas }))
		
def _despliegaEditaUsuario(self, usuario, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'usuario': usuario }))

"""
 Vista de Grupos de una Clinica en Especial
"""
def _despliegaVerGrupos(self, clinica, grupos, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'grupos': grupos,'clinica':clinica}))

"""
 Vista de Grupos de una Clinica en Especial
"""
def _despliegaVerHorarios(self, grupo, horarios, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'grupo': grupo,'horarios':horarios}))

"""
	Vista para editar Un grupo en especial
"""
def _despliegaEditaGrupo(self,clinica,grupo, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'grupo':grupo,'clinica':clinica}))


"""
	Vista para editar Un horario
"""
def _despliegaEditaHorario(self,grupo, horario, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'grupo':grupo,'horario':horario}))

def _despliegaEditaClinica(self, clinica, templateFile):
		template = env.get_template(templateFile)
		self.response.out.write(template.render({'clinica': clinica }))

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
                                #Manejo de Clinicas
                               ('/grabaClinica', GrabaClinica),
                               ('/cerrarSesion', CerrarSesion),
                               ('/grabaClinica', GrabaClinica),
                               ('/eliminaUsuario', EliminaUsuario),
                               ('/editaUsuario', EditaUsuario),
                               ('/editaClinica', EditaClinica),
                               ('/eliminaClinica', EliminaClinica),
                               ('/verClinicas', VerClinicas),
                               ('/agregarClinica', AgregarClinica),
                                #Fin manejo de Clinica
                                #Inicio de Manejo de Grupos
                               ('/verGrupos', VerGrupos),
                               ('/grabarGrupo', GrabarGrupo),
                               ('/eliminarGrupo', EliminarGrupo),
                               ('/agregarGrupo', AgregarGrupo),
                               ('/editarGrupo', EditarGrupo),
                                #Fin de manejo de Grupo
                                #Inicio de Manejo de Horarios
                               ('/verHorarios', VerHorarios),
                               ('/grabarHorario', GrabarHorario),
                               ('/eliminarHorario', EliminarHorario),
                               ('/agregarHorario', AgregarHorario),
                               ('/editarHorario', EditarHorario),
                                #Fin de manejo de Grupo
                               ('/cerrarSesion', CerrarSesion),
				('/guardaCambiosUsuario', GuardaCambiosUsuario)], debug=True)
