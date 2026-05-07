from pymongo import Mongoclient

class MongoConexion:
    def __init__(self):
        self.client = Mongoclient("mongodb://10.10.48.141:27017/")
        self.db = self.client["SistemaEmpleadosDb"]

    def obtener_coleccion(self, nombre_coleccion):
        return self.db[nombre_coleccion]
    


        