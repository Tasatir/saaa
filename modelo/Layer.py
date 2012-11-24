from Modelo import *
from ShardsCounter import *
from google.appengine.ext import db
import datetime
import time
"""from dateutil import parser"""

"""
Clase para manipulacion de Datos
del Data Store
"""

"""
Crea una Nueva Clinica
"""
@db.transactional(xg=True)
def grabaClinica(nombre,descripcion,localizacion,unidades,defectuosas):
    Clinica(nombre = nombre,
            descripcion= descripcion,
            localizacion = localizacion,
            unidades = unidades,
            defectuosas=defectuosas).put()

"""
Actualiza una clinica, proporcionando una Key para traer la entidad
"""
def actualizaClinica(key,nombre,descripcion,localizacion,unidades,defectuosas):
	if(key == None):
		return
	clinica = db.get(key)
	clinica.nombre = nombre
	clinica.descripcion = descripcion
	clinica.localizacion = localizacion
	clinica.unidades = unidades
	clinica.defectuosas = defectuosas
	clinica.put()


"""
    Elimina una Clinica y todas sus dependencias de Grupos y Horarios
"""
def eliminaClinica(key):
    clinica = db.get(key)
    #Elimina los Grupos y sus horarios en cascada
    for grupo in clinica.grupos:
        #Elimina los horarios del grupo en cascada
        for horario in grupo.horarios:
            db.delete(horario)
        db.delete(grupo)
    db.delete(clinica)


def getAllClinicas():
    return db.GqlQuery("SELECT * FROM Clinica")

"""
 Regresa todos los usuarios de la Base de Datos
"""
def getAllUsuarios():
	return db.GqlQuery("SELECT * FROM Usuario ORDER BY tipo")


"""
Regresa todos los grupos de una clinica
"""
def getAllGrupos(key):
    #Regresa la clinica
	if (key == None):
		return None
	clinica = db.get(key)
	return clinica.grupos

"""
Regresa todos los horarios de un grupo
"""
def getAllHorarios(key):
    #Regresa la clinica
	if (key == None):
		return None
	grupo = db.get(key)
	return grupo.horarios


"""
Regresa una entidad con la llave Dada
"""
def getObject(key):
		if(key == None):
			return None
		return db.get(key)

"""
	Guarda un grupo nuevo en la base de datos
"""
def grabaGrupo(clinica,nombre,descripcion,inicioAgenda,finAgenda,fa):
	if(clinica == None):
		return
	clinica = db.get(clinica)
	if(clinica == None):
		return
	i = inicioAgenda.split(':')
	f = finAgenda.split(':')
	Grupo(clinica = clinica,parent=clinica, nombre = nombre, descripcion = descripcion,inicioAgenda=datetime.time(int(i[0]),int(i[1]),0,0),finAgenda=datetime.time(int(f[0]),int(f[1]),0,0),fa = fa).put()

"""
	Actualiza un grupo ya existente en el Data Store
"""
def actualizaGrupo(key,nombre,descripcion,inicioAgenda,finAgenda,fa):
	if(key == None):
		return
	grupo = db.get(key)
	if(grupo == None):
		return
	grupo.nombre = nombre
	grupo.descripcion = descripcion
	i = inicioAgenda.split(':')
	f = finAgenda.split(':')
	grupo.fa = fa
	grupo.inicioAgenda=datetime.time(int(i[0]),int(i[1]),0,0)
	grupo.finAgenda=datetime.time(int(f[0]),int(f[1]),0,0)
	grupo.put()


"""
	Guarda un horario nuevo en la base de datos
"""
def grabaHorario(key,descripcion,dia,horaInicio,horaFin):
	i=horaInicio.split(':')
	f=horaFin.split(':')
	if(key == None or key == ""):
		return
	grupo = db.get(key)
	if(grupo == None):
		return
	Horario(grupo = grupo, parent=grupo,descripcion=descripcion,dia=dia,horaInicio=datetime.time(int(i[0]),int(i[1]),0,0),horaFin=datetime.time(int(f[0]),int(f[1]),0,0)).put()

def format_time(t):
	format = "%H:%M"
	return t.strftime(format)
"""
	Metodo para buscar los horarios por ancestro y ver
	los cambios inmediatos
"""
def getHorarios(grupo):
	query = Horario.all()
	query.ancestor(grupo)
	return query
"""
	Metodo para buscar las clinicas por ancestro
	y ver los cambios inmediatos
"""
def getGrupos(clinica):
	query = Grupo.all()
	query.ancestor(clinica)
	return query

	
"""
	Actualiza un horario ya existente en el data store
"""
def actualizaHorario(key,descripcion,dia,horaInicio,horaFin):
	if(key == None or key == ""):
		return
	horario = db.get(key)
	if(grupo == None):
		return
	horario.descripcion = descripcion
	horario.dia = dia
	i=horaInicio.split(':')
	f=horaFin.split(':')
	horario.horaInicio=datetime.time(int(i[0]),int(i[1]),0,0)
	horario.horaFin=datetime.time(int(f[0]),int(f[1]),0,0)
	horario.put()



"""
	Elimina un Grupo y sus Horarios del Data Store
"""
def eliminaGrupo(key):
	if(key == None):
		return
	grupo = db.get(key)
	if(grupo == None):
		return
	for horario in grupo.horarios:
		db.delete(horario)
	db.delete(grupo)


"""
    Elimina un Horario
"""
def eliminaHorario(key):
    horario = db.get(key)
    db.delete(horario)

"""
   Crea una asignacion de un usuario a un grupo
	Lo hace de forma transaccional
"""
@db.transactional(xg=True)
def creaAsignacion(usuario,grupo):
	if( usuario == None or usuario == "" or grupo == None or grupo == ""):
		return
	usuario = db.get(usuario)
	grupo = db.get(grupo)
	ciclo = None
	Usuario_Clinica(usuario = usuario, grupo = grupo, ciclo = ciclo).put()

def verificaDisponibilidadExample(h):
	horario = db.get(h)
	c = horario.parent().parent()
	espacio = c.unidades-c.defectuosas
	hoy = None
	if((datetime.datetime.now()).weekday() == dameNumeroDia(horario.dia,0)):
		hoy = datetime.date.today()
	else:
		hoy = datetime.date.today() + datetime.timedelta(days=1)
	key = c.nombre+"-"+h+"-"+(hoy).strftime("%Y-%m-%d")
	if(get_count(key) < espacio):
		increment(key)
		return get_count(key)
	return get_count(key)

		
def verificaDisponibilidad(h,usuario,descripcion,folio):
	horario = db.get(h)
	c = horario.parent().parent()
	lista = []
	espacio = c.unidades-c.defectuosas
	hoy = None
	if((datetime.datetime.now()).weekday() == dameNumeroDia(horario.dia,0)):
		hoy = datetime.date.today()
	else:
		hoy = datetime.date.today() + datetime.timedelta(days=1)
	key = c.nombre+"-"+h+"-"+(hoy).strftime("%Y-%m-%d")
	if(get_count(key) < espacio):
		#Si hay espacio regresa un True
		increment(key)
		Cita(usuario = db.get(usuario),horario = horario,descripcion = descripcion, folio = folio).put()
		lista.append(get_count(key))
		lista.append(True)
		return lista
	#Si no hay espacio regresa un False
	lista.append(get_count(key))	
	lista.append(False)
	return lista

def grabaUsuario(matricula,password,nombre,apellidop,apellidom,tipo):
    Usuario(matricula = matricula, password = password, nombre = nombre, apellidop = apellidop, apellidom = apellidom, tipo = tipo).put()

def deleteUsuario(usuario):
	usuario = db.get(usuario)
	db.delete(usuario)

def getUsuario(usuarioKey):
	usuario = db.get(usuarioKey)
	return usuario

def getAgendaValida(u):
	usuario = getObject(u)
	lista = getHorariosValidos(usuario)
	return db.GqlQuery("SELECT * FROM Horario WHERE __key__ IN :1",lista);

"""
Regresa el dia de manana
"""
def getHorariosValidos(usuario):
	horarios = []
	#Trae todos los grupos a los que pertenece el usuario
	grupos = db.GqlQuery("SELECT * FROM Usuario_Clinica WHERE usuario=:1",usuario.key())
	for g in grupos:
		for h in g.grupo.horarios:
			#Si se encuentran en el dia limite
			enMedio = False
			if((datetime.date.today()).weekday() == dameNumeroDia(h.dia,-1)):
				#Inicio de la agenda
				inicio = datetime.datetime.now() 
				inicio = inicio.replace(hour=g.grupo.inicioAgenda.hour,minute=g.grupo.inicioAgenda.minute)
				#Fin de la agenda
				fin = datetime.datetime.now() + datetime.timedelta(days=1)
				fin = fin.replace(hour=g.grupo.finAgenda.hour,minute=g.grupo.finAgenda.minute)
				if(inicio <= datetime.datetime.now() <= fin):
					enMedio = True
			if(((datetime.date.today()).weekday() == dameNumeroDia(h.dia,0)) and g.grupo.fa != "Mismo Dia"):
				#Inicio de la agenda
				inicio = datetime.datetime.today() - datetime.timedelta(days=1)
				inicio = inicio.replace(hour=g.grupo.inicioAgenda.hour,minute=g.grupo.inicioAgenda.minute)
				#Fin de la agenda
				fin = datetime.datetime.today()
				fin = fin.replace(hour=g.grupo.finAgenda.hour,minute=g.grupo.finAgenda.minute)
				if(inicio <= datetime.datetime.now() <= fin):
					enMedio = True
			if(enMedio == True):
				horarios.append(h.key())
	return horarios


def dameNumeroDia(d,i):
	if(d == "Lunes"):
		return 1+i
	if(d == "Martes"):
		return 2+i
	if(d == "Miercoles"):
		return 3+i
	if(d == "Jueves"):
		return 4+i
	if(d == "Viernes"):
		return 5+i
	if(d == "Sabado"):
		if(6+i > 6):
			return 0
		else:
			return 6+i
	if(d == "Domingo"):
		if(0+i < 0):
			return 6
		else:
			return 0+i
