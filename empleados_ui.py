from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class empleados_ui(QWidget):
    def __init__(self):
        super().__init__()
        
        # Cargar el archivo .ui
        loader = QUiLoader()
        interfaz = QFile("ui/empleados.ui") # Verifica que esta ruta sea correcta
        

        if interfaz.open(QFile.ReadOnly):
            self.ui = loader.load(interfaz, self)
            interfaz.close()
            print("Archivo .ui cargado correctamente.")
        else:
            print("¡Error! No se pudo encontrar el archivo .ui")