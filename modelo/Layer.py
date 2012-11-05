from Modelo import *
from google.appengine.ext import db
import datetime
import time
from dateutil import parser

"""
Clase para manipulacion de Datos
del Data Store
"""
def grabaClinica(nombre):
    Clinica(nombre = nombre,localizacion = "Ninguna",unidades = 1).put()

def getAllClinicas():
    return db.GqlQuery("SELECT * FROM Clinica")

def verHorarios(clinica):
    #Regresa la clinica
    clinica = db.get(clinica)
    return clinica.horarios
    
def setHorario(clinica,horaInicio,horaFin,dia,descripcion):
    format="%H:%M"
    #h1=datetime.datetime.strptime(horaInicio+":00","%H:%M:%S")
    h2=time.strptime(horaInicio, format)
    Horario(grupo=db.get(clinica),descripcion=descripcion,dia=dia,horaInicio=datetime.time(10,10,10,0)).put()
	

