from Modelo import *
from google.appengine.ext import db
import datetime
import time

"""
Clase para manipulacion de Datos
del Data Store
"""
def updateUsuario(usuario,pnombre,pmatricula,papellidop,papellidom,ptipo):
	"""usuario = db.get(pusuario)"""
	usuario.nombre = pnombre
	usuario.matricula = pmatricula
	usuario.apellidop = papellidop
	usuario.apellidom = papellidom
	usuario.tipo = ptipo
	usuario.put()
	
