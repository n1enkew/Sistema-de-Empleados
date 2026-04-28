from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from ui.empleados_ui import Empleados_ui
from ui.dptos_ui import Dptos_ui

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # cargar Interfaz.ui --- DASHBOARD PRINCIPAL ---
        loader = QUiLoader()
        interfaz = QFile("ui/interfaz.ui") # Verifica que esta ruta sea correcta
        
        if interfaz.open(QFile.ReadOnly):
            print("Archivo .ui cargado correctamente.")
        else:
            print("¡Error! No se pudo encontrar el archivo .ui")

        # Crear la interfaz basada en el diseño
        self.ui = loader.load(interfaz, self)
        interfaz.close()

        # Ajustar tamano al de qt
        self.resize(self.ui.size())
        self.setMinimumSize(self.ui.size())
        
        # Configurar la ventana
        self.setCentralWidget(self.ui.centralwidget)
        self.setWindowTitle("Sistema de Empleados - Dashboard")

        # Conectar botones a funciones
        # Ejemplo: self.ui.nombre_de_tu_boton.clicked.connect(self.una_funcion)
        self.ui.btn_empleados.clicked.connect(self.cambiar_a_empleados)
        self.ui.btn_dptos.clicked.connect(self.cambiar_a_departamentos)
        self.ui.btn_proyectos.clicked.connect(self.cambiar_a_proyectos)
        self.ui.btn_informes.clicked.connect(self.cambiar_a_informes)
        self.ui.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)

        # empleados_ui.py --- INTERFAZ DE EMPLEADOS CRUD ---
        self.seccion_empleados = Empleados_ui()
        self.seccion_dptos = Dptos_ui()
        
        # 2. La metemos dentro del QStackedWidget de tu diseño
        # El stack_paginas es el que está dentro del frame_9
        self.ui.stack_paginas.addWidget(self.seccion_empleados)
        self.ui.stack_paginas.addWidget(self.seccion_dptos)
        
        # 3. Obtenemos el número de página donde quedó
        self.indice_empleados = self.ui.stack_paginas.indexOf(self.seccion_empleados)
        self.indice_dptos = self.ui.stack_paginas.indexOf(self.seccion_dptos)
        

    # 4. Funciones para cambiar de página en el QStackedWidget
    def cambiar_a_empleados(self):
        self.ui.stack_paginas.setCurrentIndex(self.indice_empleados)
        print("Cambiando a vista de Empleados...")

    def cambiar_a_departamentos(self):
        self.ui.stack_paginas.setCurrentIndex(self.indice_dptos)
        print("Cambiando a vista de Departamentos...")

    def cambiar_a_proyectos(self):
        # Si tienes más páginas, solo sigue el orden del índice (0, 1, 2, ...)
        self.ui.stack_paginas.setCurrentIndex(2)
        print("Cambiando a vista de Proyectos...")

    def cambiar_a_informes(self):
        self.ui.stack_paginas.setCurrentIndex(3)
        print("Cambiando a vista de Informes...")

    def cerrar_sesion(self):
        print("Cerrando sesión...")
        self.close()