from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from datetime import datetime

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

    def crear_empleado(self):
        try:
            nombre = self.ui.r_nombre.text()
            # Combinamos calle y ciudad en un solo string para la columna 'direccion'
            direccion = f"{self.ui.r_calle.text()}, {self.ui.r_ciudad.text()}"
            
            fecha_qdate = self.ui.r_fecha_inicio.date()
            fecha_dt = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())

            # IMPORTANTE: Aquí deberías pasar el ID del depto, no el nombre.
            # Por ahora pasaremos 1 como prueba o el index del combobox
            id_depto = self.ui.r_dpto_asig.currentIndex() + 1 

            exito = self.modelo_empleado.crear_empleado(
                nombre, 
                direccion, 
                self.ui.r_telefono.text(),
                self.ui.r_correo.text(),
                fecha_dt,
                float(self.ui.r_salario.text() or 0),
                id_depto
            )
            
            if exito:
                print(f"Empleado {nombre} guardado en MySQL.")
                self.limpiar_formulario()
        
        except Exception as e:
            print(f"Error en la interfaz: {e}")