from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from datetime import datetime
from database.EmpleadoModel import EmpleadoModel

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

        self.modelo_empleado = EmpleadoModel() 

        # Ajustar tamaño al de qt
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.addWidget(self.ui) # 'self.ui' es lo que cargó el loader

        self.ui.btn_registrar.clicked.connect(self.sec_registrar_empleado)
        self.ui.btn_modificar_eliminar.clicked.connect(self.sec_modificar_eliminar_empleado)
        self.ui.btn_mostrar.clicked.connect(self.sec_mostrar_empleados)

        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0)) # Para que se abra en la seccion de registrar empleado por defecto

    def sec_registrar_empleado(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0))
        print("Registrar empleado")

    def sec_modificar_eliminar_empleado(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(1))
        print("Modificar/Eliminar empleado")

    def sec_mostrar_empleados(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(2))
        print("Mostrar empleados")

    def registrar_empleado(self):
        nombre = self.ui.input_nombre.text()
        calle = self.ui.input_calle.text()
        ciudad = self.ui.txt_ciudad.text()

        datos_direccion = {
        "calle": calle,
        "ciudad": ciudad,
        "region": "Atacama"
    }
    
        fecha_dt = datetime.strptime("%d/%m/%Y")

        self.modelo_empleado.crear_empleado(
            nombre, 
            datos_direccion, 
            self.ui.txt_tel.text(),
            self.ui.txt_correo.text(),
            fecha_dt,
            self.ui.txt_salario.text(),
            self.ui.cbx_depto.currentText() # Si usas un ComboBox para el depto
        )
    