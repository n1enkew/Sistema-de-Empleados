import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMdiSubWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargar la ventana principal (el Dashboard)
        loader = QUiLoader()
        archivo_principal = QFile("dashboard_interfaz.ui")
        archivo_principal.open(QFile.ReadOnly)
        loader.load(archivo_principal, self)
        archivo_principal.close()
        
        self.setCentralWidget(self)
        self.setWindowTitle("Sistema de Empleados - Atacalma")

        # Conectar el botón para abrir la ventana de registro
        # (Asegúrate de que el nombre del botón coincida con el del Designer)
        self.btn_nuevo_empleado.clicked.connect(self.abrir_registro)
        self.show()

    def abrir_registro(self):
        # 1. Cargamos el segundo archivo .ui (la ventana hija)
        loader = QUiLoader()
        archivo_hija = QFile("ui/registro_empleado.ui")
        
        if not archivo_hija.open(QFile.ReadOnly):
            print("Error: No se pudo abrir el archivo de registro")
            return
            
        # Este 'widget_hijo' contiene todo lo que diseñaste en el segundo .ui
        widget_hijo = loader.load(archivo_hija)
        archivo_hija.close()
        
        # 2. Creamos el contenedor MDI
        subventana = QMdiSubWindow()
        subventana.setWidget(widget_hijo) # Metemos el .ui cargado dentro
        subventana.setWindowTitle("Registro de Nuevo Empleado")
        
        # 3. Lo agregamos al área MDI del Dashboard
        # Suponiendo que tu QMdiArea se llama 'area_trabajo'
        self.ui.area_trabajo.addSubWindow(subventana)
        
        # 4. Mostrar
        subventana.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())