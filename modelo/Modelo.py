from google.appengine.ext import db
"""
Modelo del Proyecto
"""
class Clinica(db.Model):
    #Nombre de la clinica (Ejemplo: Laboratorio de Coronas 3)
    nombre = db.StringProperty(required = True)
    #Alguna descripcion, no es necesaria
    descripcion = db.StringProperty()
    #La localizacion dentro de la facultad
    localizacion = db.StringProperty(required = True)
    #Numero de unidades en la clinica
    unidades = db.IntegerProperty(required = True)
    #Numero de unidades defectuosas y su numero de unidad
    defectuosas = db.ListProperty(int)

#Usuarios, qu epueden ser alumnos, doctores, encargados o administradores
class Usuario(db.Model):
    #ID del usuario que es dueno de esta entidad
    #En este caso es la matricula
    matricula = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    # Informacion basica
    nombre = db.StringProperty(required = True)
    apellidop = db.StringProperty(required = True)
    apellidom = db.StringProperty(required = True)
    #Tipo de Usuario
    tipo = db.StringProperty()

#Ciclos escolares
class Ciclo(db.Model):
    validFrom = db.DateProperty(required = True)
    validTo = db.DateProperty(required = True)
    descripcion = db.StringProperty(required = True)
    isActual = db.BooleanProperty(required = True,default = 0)

#Grupos en los que se Dividen las clinicas
class Grupo(db.Model):
    clinica = db.ReferenceProperty(Clinica,collection_name='grupos')
    nombre = db.StringProperty(required = True)
    descripcion = db.StringProperty(required = True)

#Horarios de los Grupos
class Horario(db.Model):
    grupo = db.ReferenceProperty(Grupo,collection_name='horarios')
    descripcion = db.StringProperty(required = True)
    dia = db.StringProperty(required = True, choices=('Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo'))
    horaInicio = db.TimeProperty(required = True)
    horaFin = db.TimeProperty(required = True)

#Relacion de Usuarios con Clinicas
class Usuario_Clinica(db.Model):
    usuario = db.ReferenceProperty(Usuario,required=True,collection_name='grupos')
    grupo = db.ReferenceProperty(Grupo,required=True,collection_name='usuarios')
    #El ciclo escolar del usuario
    ciclo = db.ReferenceProperty(Ciclo,required=True)
    #El usuario es aceptado en la clinica para este ciclo
    isAccepted = db.BooleanProperty(required = True,default = 0)

#Horarios de los Grupos
class Cita(db.Model):
    usuario = db.ReferenceProperty(Usuario,collection_name='citas')
    horario = db.ReferenceProperty(Horario,collection_name='pacientes')
    descripcion = db.StringProperty(required = True)
    folio = db.StringProperty(required = True)
    dia = db.StringProperty(required = True, choices=('Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo'))
    hora = db.TimeProperty(required = True)
