from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class Dptos_ui(QWidget):
    def __init__(self):
        super().__init__()

        # Cargar el archivo .ui
        loader = QUiLoader()
        interfaz = QFile("ui/dptos.ui")

        if interfaz.open(QFile.ReadOnly):
            self.ui = loader.load(interfaz, self)
            interfaz.close()
            print("Archivo .ui cargado correctamente.")
        else:
            print("¡Error! No se pudo encontrar el archivo .ui")

        # Ajuste de tamano
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.addWidget(self.ui) # 'self.ui' es lo que cargó el loader

        # Conectar botones
        self.ui.btn_registrar.clicked.connect(self.registrar_departamento)
        self.ui.btn_modificar_eliminar.clicked.connect(self.modificar_eliminar_departamento)
        self.ui.btn_mostrar.clicked.connect(self.mostrar_departamentos)
        
        # Para que se abra en la seccion de registrar departamento por defecto
        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(0))

        # agregar las secciones al QStackedWidget
        # self.ui.stack_dpto.addWidget(self.seccion_registrar)
        # self.ui.stack_dpto.addWidget(self.seccion_modificar_eliminar)
        # self.ui.stack_dpto.addWidget(self.seccion_mostrar)

        # numero de pagina
        # self.indice_registrar = self.ui.stack_dpto.indexOf(self.seccion_registrar)
        # self.indice_modificar_eliminar = self.ui.stack_dpto.indexOf(self.seccion_modificar_eliminar)
        # self.indice_mostrar = self.ui.stack_dpto.indexOf(self.seccion_mostrar)

    def registrar_departamento(self):
        print("----")
        print(type(self.ui.stack_dpto.widget(0)))
        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(0))
        print("Registrar departamento")
    
    def modificar_eliminar_departamento(self):
        print("----")
        print(type(self.ui.stack_dpto.widget(1)))
        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(1))
        print("Modificar/Eliminar departamento")

    def mostrar_departamentos(self):
        print("----")
        print(type(self.ui.stack_dpto.widget(2)))
        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(2))
        print("Mostrar departamentos")

                