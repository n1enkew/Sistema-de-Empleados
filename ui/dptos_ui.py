from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from database.DptoModel import DepartamentoModel

class Dptos_ui(QWidget):
    def __init__(self):
        super().__init__()
        self.modelo_dep = DepartamentoModel()

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

        self.modelo_tabla = QStandardItemModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.modelo_tabla)
        self.ui.tabla_dptos.setModel(self.proxy_model)

        # Conectar botones
        self.ui.btn_registrar.clicked.connect(self.registrar_departamento)
        self.ui.btn_modificar_eliminar.clicked.connect(self.modificar_eliminar_departamento)
        self.ui.btn_mostrar.clicked.connect(self.mostrar_departamentos)

        self.ui.btn_guardar_dpto.clicked.connect(self.ejecutar_registro)
        self.ui.btn_eliminar_dpto.clicked.connect(self.ejecutar_eliminacion)
        self.ui.btn_guardar_mod.clicked.connect(self.ejecutar_modificacion)

        

        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(0))
        self.aplicar_estilo_tabla()
        self.ui.cbx_mod_depto.currentIndexChanged.connect(self.cargar_datos_en_campos)

    def registrar_departamento(self):
        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(0))
        print("Registrar departamento")
    
    def modificar_eliminar_departamento(self):
        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(1))
        self.preparar_modificacion()
        print("Modificar/Eliminar departamento")

    def mostrar_departamentos(self):
        self.ui.stack_dpto.setCurrentWidget(self.ui.stack_dpto.widget(2))
        self.mostrar_tabla()
        print("Mostrar departamentos")

    def ejecutar_registro(self):
        nom = self.ui.r_nombre.text()
        ger = self.ui.r_gerente.text()

        if not nom or not ger:
            QMessageBox.warning(self, "Campos vacíos", "Por favor rellene todos los campos.")
            return

        if self.modelo_dep.crear(nom, ger):
            QMessageBox.information(self, "Éxito", "Departamento creado.")
            self.ui.r_nombre.clear()
            self.ui.r_gerente.clear()

    def preparar_modificacion(self):
        self.ui.stack_dpto.setCurrentIndex(1)
        deptos = self.modelo_dep.consultar_todos()
        self.ui.cbx_mod_depto.clear()
        self.ui.m_nombre.clear()
        self.ui.m_gerente.clear()
        for d in deptos:
            self.ui.cbx_mod_depto.addItem(d['nombre'], d['idDepartamento'])

    def cargar_datos_en_campos(self):
        id_d = self.ui.cbx_mod_depto.currentData()
        if id_d:
            deptos = self.modelo_dep.consultar_todos()
            # Buscamos el depto específico en la lista
            depto = next((x for x in deptos if x['idDepartamento'] == id_d), None)
            if depto:
                self.ui.m_nombre.setText(depto['nombre'])
                self.ui.m_gerente.setText(depto['gerente'])

    def ejecutar_modificacion(self):
        id_d = self.ui.cbx_mod_depto.currentData()
        nom = self.ui.m_nombre.text()
        ger = self.ui.m_gerente.text()
        if self.modelo_dep.actualizar(id_d, nom, ger):
            QMessageBox.information(self, "Éxito", "Departamento actualizado.")
            self.preparar_modificacion()

    def ejecutar_eliminacion(self):
        id_d = self.ui.cbx_mod_depto.currentData()
        if id_d and QMessageBox.question(self, "Confirmar", "¿Eliminar depto?") == QMessageBox.Yes:
            if self.modelo_dep.eliminar(id_d):
                QMessageBox.information(self, "Éxito", "Eliminado.")
                self.preparar_modificacion()
            else:
                QMessageBox.critical(self, "Error", "No se puede eliminar: Tiene empleados asociados.")

    def mostrar_tabla(self):
        self.ui.stack_dpto.setCurrentIndex(2)
        datos = self.modelo_dep.consultar_todos()
        self.modelo_tabla.clear()
        self.modelo_tabla.setHorizontalHeaderLabels(["ID", "Departamento", "Gerente"])
        for d in datos:
            self.modelo_tabla.appendRow([
                QStandardItem(str(d['idDepartamento'])),
                QStandardItem(d['nombre']),
                QStandardItem(d['gerente'])
            ])
        self.ui.tabla_dptos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def aplicar_estilo_tabla(self):
        self.ui.tabla_dptos.setStyleSheet("""
            QTableView {
                background-color: rgb(44, 32, 22);
                color: white;
                gridline-color: rgb(70, 55, 40);
                border: 1px solid rgb(80, 60, 45);
                border-radius: 5px;
                selection-background-color: rgb(117, 93, 72);
            }
            QHeaderView::section {
                background-color: rgb(30, 22, 15);
                color: #D2B48C;
                padding: 8px;
                border: 1px solid rgb(60, 45, 35);
                font-weight: bold;
            }
            QTableView::item:hover {
                background-color: rgb(85, 65, 50);
            }
        """)
                