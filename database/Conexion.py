from pymongo import MongoClient

class MongoConexion:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["SistemaEmpleadosDb"]

    def obtener_coleccion(self, nombre_coleccion):
        return self.db[nombre_coleccion]
    


        