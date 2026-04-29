from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from ui.empleados_ui import Empleados_ui
from ui.dptos_ui import Dptos_ui
from ui.proyectos_ui import Proyectos_ui
from ui.informes_ui import Informes_ui
from ui.horarios_ui import Horarios_ui

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # cargar Interfaz.ui --- DASHBOARD PRINCIPAL ---
        loader = QUiLoader()
        interfaz = QFile("ui/interfaz.ui")
        
        if interfaz.open(QFile.ReadOnly):
            print("Archivo .ui cargado correctamente.")
        else:
            print("¡Error! No se pudo encontrar el archivo .ui")

        # Crear la interfaz basada en el diseño
        self.ui = loader.load(interfaz, self)
        interfaz.close()

        # Ajustar tamano
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
        self.ui.btn_horarios.clicked.connect(self.cambiar_a_horarios)

        # --- INTERFAZ CRUD (Empleados Departamentos Proyectos Informes) ---
        self.seccion_inicio = QWidget()
        self.seccion_empleados = Empleados_ui()
        self.seccion_dptos = Dptos_ui()
        self.seccion_proyectos = Proyectos_ui()
        self.seccion_informes = Informes_ui()
        self.seccion_horarios = Horarios_ui()

        # 2. La metemos dentro del QStackedWidget
        self.ui.stack_paginas.addWidget(self.seccion_inicio)
        self.ui.stack_paginas.addWidget(self.seccion_empleados)
        self.ui.stack_paginas.addWidget(self.seccion_dptos)
        self.ui.stack_paginas.addWidget(self.seccion_proyectos)
        self.ui.stack_paginas.addWidget(self.seccion_informes)
        self.ui.stack_paginas.addWidget(self.seccion_horarios)
        
        # 3. Obtenemos el número de página donde quedó
        self.indice_inicio = self.ui.stack_paginas.indexOf(self.seccion_inicio)
        self.indice_empleados = self.ui.stack_paginas.indexOf(self.seccion_empleados)
        self.indice_dptos = self.ui.stack_paginas.indexOf(self.seccion_dptos)
        self.indice_proyectos = self.ui.stack_paginas.indexOf(self.seccion_proyectos)
        self.indice_informes = self.ui.stack_paginas.indexOf(self.seccion_informes)
        self.indice_horarios = self.ui.stack_paginas.indexOf(self.seccion_horarios)

            
    # Función para mostrar la página de inicio al desmarcar los botones
    def limpiar_botones(self, boton_activo):
        # Lista de todos tus botones del menú
        botones = [self.ui.btn_empleados, self.ui.btn_dptos, self.ui.btn_proyectos, self.ui.btn_informes, self.ui.btn_horarios]
        
        for btn in botones:
            if btn != boton_activo:
                btn.setChecked(False)

    # 4. Funciones para cambiar de página en el QStackedWidget
    def cambiar_a_empleados(self):
        if self.ui.btn_empleados.isChecked():
            self.limpiar_botones(self.ui.btn_empleados)
            self.ui.stack_paginas.setCurrentIndex(self.indice_empleados)
            self.ui.label_2.setText("Gestion de Empleados")
            print("Cambiando a vista de Empleados...")
        else:
            self.ui.stack_paginas.setCurrentIndex(self.indice_inicio)
            self.ui.label_2.setText("Menu Principal")
            print("Volviendo al Dashboard Principal...")

    def cambiar_a_departamentos(self):
        if self.ui.btn_dptos.isChecked():
            self.limpiar_botones(self.ui.btn_dptos)
            self.ui.stack_paginas.setCurrentIndex(self.indice_dptos)
            self.ui.label_2.setText("Gestion de Departamentos")
            print("Cambiando a vista de Departamentos...")
        else:
            self.ui.stack_paginas.setCurrentIndex(self.indice_inicio)
            self.ui.label_2.setText("Menu Principal")
            print("Volviendo al Dashboard Principal...")

    def cambiar_a_proyectos(self):
        if self.ui.btn_proyectos.isChecked():
            self.limpiar_botones(self.ui.btn_proyectos)
            self.ui.stack_paginas.setCurrentIndex(self.indice_proyectos)
            self.ui.label_2.setText("Gestion de Proyectos")
            print("Cambiando a vista de Proyectos...")
        else:
            self.ui.stack_paginas.setCurrentIndex(self.indice_inicio)
            self.ui.label_2.setText("Menu Principal")
            print("Volviendo al Dashboard Principal...")

    def cambiar_a_informes(self):
        if self.ui.btn_informes.isChecked():
            self.limpiar_botones(self.ui.btn_informes)
            self.ui.stack_paginas.setCurrentIndex(self.indice_informes)
            self.ui.label_2.setText("Gestion de Informes")
            print("Cambiando a vista de Informes...")
        else:
            self.ui.stack_paginas.setCurrentIndex(self.indice_inicio)
            self.ui.label_2.setText("Menu Principal")
            print("Volviendo al Dashboard Principal...")

    def cambiar_a_horarios(self):
        if self.ui.btn_horarios.isChecked():
            self.limpiar_botones(self.ui.btn_horarios)
            self.ui.stack_paginas.setCurrentIndex(self.indice_horarios)
            self.ui.label_2.setText("Gestion de Horarios")
            print("Cambiando a vista de Horarios...")
        else:
            self.ui.stack_paginas.setCurrentIndex(self.indice_inicio)
            self.ui.label_2.setText("Menu Principal")
            print("Volviendo al Dashboard Principal...")

    def cerrar_sesion(self):
        print("Cerrando sesión...")
        self.close()

