import sys
import ctypes
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from ui.dashboard import Dashboard # Importamos tu clase desde el otro archivo


if __name__ == "__main__":
    # Creamos el motor de la aplicación
    myappid = 'sistemaempleados.sql' # Reemplaza con tu propio ID de aplicación
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)

    # icono barra de tareas
    app.setWindowIcon(QIcon("assets/img/snowflake_2744-fe0f.png"))
    
    # Creamos la instancia de nuestra ventana
    ventana_principal = Dashboard()
    ventana_principal.show()

    # icono de la ventana
    ventana_principal.setWindowIcon(QIcon("assets/img/snowflake_2744-fe0f.png"))

    # Para mostrar la ventana maximizada al iniciar
    ventana_principal.showMaximized()
    
    # Iniciamos el bucle de eventos
    sys.exit(app.exec())