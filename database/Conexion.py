import mysql.connector
from mysql.connector import Error

class MySQLConexion:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',       # Tu usuario
            'password': '123456', # Tu contraseña
            'database': 'secdb'
        }

    def obtener_conexion(self):
        try:
            conexion = mysql.connector.connect(**self.config)
            return conexion
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None