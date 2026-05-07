from database.Conexion import MongoConexion
from datetime import datetime

class EmpleadoModel:
    def __init__(self):
        self.conexion = MongoConexion()
        self.coleccion_empleados = self.conexion.obtener_coleccion("empleados")

    def crear_empleado(self, nombre, direccion_dict, telefono, correo, fecha_inicio, salario, depto):
        """
        direccion_dict debe ser un diccionario: 
        {"calle": "Los Carrera", "ciudad": "Copiapó", "region": "Atacama"}
        """
        
        # Este es el "Documento" que se guardará en MongoDB
        documento = {
            "nombre": nombre,
            "direccion": { # Esto es un SUBDOCUMENTO
                "calle": direccion_dict.get("calle", ""),
                "ciudad": direccion_dict.get("ciudad", ""),
                "region": direccion_dict.get("region", "")
            },
            "contacto": { # También podemos agrupar contacto si quieres
                "telefono": telefono,
                "correo": correo
            },
            "fecha_inicio": fecha_inicio, # Se recomienda guardar como objeto datetime
            "salario": float(salario),
            "departamento": depto,
            "estado": "activo"
        }
        
        return self.coleccion.insert_one(documento)