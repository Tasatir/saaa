from Modelo import *
from google.appengine.ext import db
import datetime
import time
"""from dateutil import parser
"""

"""
Clase para manipulacion de Datos
del Data Store
"""
def grabaClinica(nombre):
    Clinica(nombre = nombre,localizacion = "Ninguna",unidades = 1).put()

def getAllClinicas():
    return db.GqlQuery("SELECT * FROM Clinica")

def verGrupos(clinica):
    #Regresa la clinica
    clinica = db.get(clinica)
    return clinica.grupos
    
def setHorario(grupo,horaInicio,horaFin,dia,descripcion):
    format="%H:%M"
    #h1=datetime.datetime.strptime(horaInicio+":00","%H:%M:%S")
    h2=time.strptime(horaInicio, format)
    Horario(grupo=db.get(clinica),descripcion=descripcion,dia=dia,horaInicio=datetime.time(10,10,10,0),horaFin=datetime.time(10,10,10,0)).put()

def deleteHorario(horario):
    horario = db.get(horario)
    db.delete(horario)

def grabaUsuario(matricula,password,nombre,apellidop,apellidom,tipo):
    Usuario(matricula = matricula, password = password, nombre = nombre, apellidop = apellidop, apellidom = apellidom, tipo = tipo).put()

def deleteUsuario(usuario):
	usuario = db.get(usuario)
	db.delete(usuario)

def getUsuario(usuario):
	usuario = db.get(usuario)
	return usuario

def updateUsuario(pusuario,pnombre,pmatricula,papellidop,papellidom,ptipo):
	usuario = db.get(pusuario)
	usuario.nombre = pnombre
	usuario.matricula = pmatricula
	usuario.apellidop = papellidop
	usuario.apellidom = papellidom
	usuario.tipo = ptipo
	usuario.put()
	
