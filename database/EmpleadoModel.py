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

    def consultar_todos_lista(self):
        conexion = self.db.obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            # Solo traemos ID y Nombre para el ComboBox
            cursor.execute("SELECT idEmpleado, nombre FROM Empleado")
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()
            return resultados

    def consultar_por_id(self, id_emp):
        conexion = self.db.obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Empleado WHERE idEmpleado = %s", (id_emp,))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            return resultado

    def actualizar_empleado(self, id_emp, nombre, direccion, tel, correo, fecha, salario, id_depto):
        conexion = self.db.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """UPDATE Empleado SET 
                         nombre=%s, direccion=%s, telefono=%s, correo=%s, 
                         fecha_inicio=%s, salario=%s, Departamento_idDepartamento=%s 
                         WHERE idEmpleado=%s"""
                valores = (nombre, direccion, tel, correo, fecha, salario, id_depto, id_emp)
                cursor.execute(sql, valores)
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def eliminar_empleado(self, id_emp):
        conexion = self.db.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "DELETE FROM Empleado WHERE idEmpleado = %s"
                cursor.execute(sql, (id_emp,))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar en SQL: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()