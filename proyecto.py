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
import os
import cgi
import datetime
import urllib
import modelo.Layer
#Framework de Web para Python
import webapp2
                                  
# API DataStore
from google.appengine.ext import db

# intitalization of template system. It says that HTML templates will
# be found in current directory ("__file__")
jinja_environment = jinja2.Environment( \
   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

"""
REQUEST HANDLERS
"""

class MainPage(webapp2.RequestHandler):
    """Pantalla inicial. Despliega la lista de Productos
       Entrada: El usuario ha ingresado a a la aplicacion.
                Base de datos puede tener ya datos de productos.
       Salida: Se ha desplegado:
				Lista de productos con opcion de editar,eliminar y nuevo
    """
            
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        #productos = db.GqlQuery("SELECT * FROM Producto")
        
        respuesta = "Hola"
        self.response.out.write(respuesta)
        # Estos son los productos
        # Despliega los productos, el nombre, descripcion y la cantidad
        # Se pone una liga de editar al lado de los productos
        # Al final de la lista, una liga de Agrega Producto


app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
