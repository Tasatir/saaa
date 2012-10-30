from Modelo import *
from google.appengine.ext import db
import datetime
import time
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
    

