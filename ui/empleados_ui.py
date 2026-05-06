from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class Empleados_ui(QWidget):
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

        # Ajustar tamaño al de qt
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.addWidget(self.ui) # 'self.ui' es lo que cargó el loader

        self.ui.btn_registrar.clicked.connect(self.registrar_empleado)
        self.ui.btn_modificar_eliminar.clicked.connect(self.modificar_eliminar_empleado)
        self.ui.btn_mostrar.clicked.connect(self.mostrar_empleados)

        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0)) # Para que se abra en la seccion de registrar empleado por defecto

    def registrar_empleado(self):
        print("----")
        print(type(self.ui.stack_empleado.widget(0)))
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0))
        print("Registrar empleado")

    def modificar_eliminar_empleado(self):
        print("----")
        print(type(self.ui.stack_empleado.widget(1)))
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(1))
        print("Modificar/Eliminar empleado")

    def mostrar_empleados(self):
        print("----")
        print(type(self.ui.stack_empleado.widget(2)))
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(2))
        print("Mostrar empleados")