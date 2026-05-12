from database.Conexion import MySQLConexion

class DepartamentoModel:
    def __init__(self):
        self.db = MySQLConexion()

    def crear(self, nombre, gerente):
        conexion = self.db.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO Departamento (nombre, Gerente) VALUES (%s, %s)"
                cursor.execute(sql, (nombre, gerente))
                conexion.commit()
                return True
            finally:
                cursor.close()
                conexion.close()
        return False

    def consultar_todos(self):
        conexion = self.db.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Departamento")
                return cursor.fetchall()
            finally:
                cursor.close()
                conexion.close()
        return []

    def actualizar(self, id_depto, nombre, gerente):
        conexion = self.db.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "UPDATE Departamento SET nombre=%s, Gerente=%s WHERE idDepartamento=%s"
                cursor.execute(sql, (nombre, gerente, id_depto))
                conexion.commit()
                return True
            finally:
                cursor.close()
                conexion.close()
        return False

    def eliminar(self, id_depto):
        conexion = self.db.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "DELETE FROM Departamento WHERE idDepartamento = %s"
                cursor.execute(sql, (id_depto,))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error: No puedes eliminar un depto con empleados activos. {e}")
                return False
            finally:
                cursor.close()
                conexion.close()
        return False