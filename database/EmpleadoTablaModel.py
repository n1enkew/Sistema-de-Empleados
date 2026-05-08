from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from datetime import datetime

class EmpleadoTableModel(QAbstractTableModel):
    def __init__(self, datos=None):
        super().__init__()
        self._datos = datos or []
        # Definimos las cabeceras de la tabla
        self._headers = ["Nombre", "Calle", "Ciudad", "Teléfono", "Correo", "Salario", "Fecha de Inicio", "Departamento"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._datos)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        empleado = self._datos[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            # Aquí mapeamos cada columna a los datos de MongoDB
            if col == 0: return empleado.get("nombre")
            if col == 1: return empleado.get("direccion", {}).get("calle")
            if col == 2: return empleado.get("direccion", {}).get("ciudad")
            if col == 3: return empleado.get("contacto", {}).get("telefono")
            if col == 4: return empleado.get("contacto", {}).get("correo")
            if col == 5: return f"$ {empleado.get('salario', 0):,.0f}" # Formato moneda
            if col == 6: return empleado.get("fecha_inicio")
            if col == 7: return empleado.get("departamento")

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None