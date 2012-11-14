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

def to_datetime(s):
  return datetime.date(*time.strptime(s, "%m/%d/%Y")[0:3])
  
def grabaPeriodo(descripcion,fechaInicio,fechaFin,actual):
	Ciclo(validFrom = fechaInicio,
		validTo = fechaFin,
		descripcion = descripcion,
		isActual = actual).put()

def quitaActual():
	periodos = db.GqlQuery("SELECT * FROM Ciclo WHERE isActual = True")
	for periodo in periodos:
		periodo.isActual = False
		periodo.put()

def getAllPeriodos():
	periodos = db.GqlQuery("SELECT * FROM Ciclo")
	return periodos

def deletePeriodo(periodoKey):
	periodo = db.get(periodoKey)
	db.delete(periodo)

def getPeriodo(periodoKey):
	periodo = db.get(periodoKey)
	return periodo

def updatePeriodo(periodo,pdescripcion,pfi,pff,pesActual):
	periodo.descripcion = pdescripcion
	periodo.validFrom = pfi
	periodo.validTo = pff
	periodo.isActual = pesActual
	periodo.put()
