from database.Conexion import MySQLConexion

class EmpleadoModel:
    def __init__(self):
        self.db = MySQLConexion()

    def crear_empleado(self, nombre, direccion, telefono, correo, fecha, salario, id_depto):
        conexion = self.db.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO Empleado 
                         (nombre, direccion, telefono, correo, fecha_inicio, salario, Departamento_idDepartamento) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                
                valores = (nombre, direccion, telefono, correo, fecha, salario, id_depto)
                cursor.execute(sql, valores)
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error SQL: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()