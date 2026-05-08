import csv
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from datetime import datetime
from database.EmpleadoModel import EmpleadoModel

class Importes_ui(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Cargar el archivo .ui
        loader = QUiLoader()
        interfaz = QFile("ui/importes.ui")
        if interfaz.open(QFile.ReadOnly):
            self.ui = loader.load(interfaz, self)
            interfaz.close()

        self.modelo_empleado = EmpleadoModel()

        # 2. Configuración de Layout
        # Ajustamos el .ui al widget principal (como hiciste en empleados_ui)
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.addWidget(self.ui)

        # 3. Inyectar botón de importación por código
        # Lo ponemos dentro de tu frame de la imagen (ajusta el nombre si es distinto)
        self.btn_abrir_csv = QPushButton("Seleccionar Archivo CSV")
        self.btn_abrir_csv.setMinimumHeight(60)
        self.btn_abrir_csv.setStyleSheet("""
            QPushButton {
                background-color: rgb(117, 93, 72);
                color: white;
                font-weight: bold;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgb(137, 113, 92);
            }
        """)

        # Si tu frame se llama 'frame_importar', lo añadimos ahí
        # Si no tiene layout, le creamos uno
        if self.ui.frame_2.layout() is None:
            self.ui.frame_2.setLayout(QVBoxLayout())
        
        self.ui.frame_2.layout().addStretch()
        self.ui.frame_2.layout().addWidget(self.btn_abrir_csv)
        self.ui.frame_2.layout().addStretch()

        # 4. Conexión del botón
        self.btn_abrir_csv.clicked.connect(self.sistema_importacion)

    def sistema_importacion(self):
        # A. Abrir cuadro de diálogo para buscar el archivo
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar CSV", 
            "", 
            "Archivos CSV (*.csv)"
        )

        if not ruta_archivo:
            return # El usuario canceló la selección

        # B. Iniciar el procesamiento
        self.procesar_csv(ruta_archivo)

    def procesar_csv(self, ruta):
        try:
            empleados_a_importar = []
            
            with open(ruta, mode='r', encoding='utf-8') as archivo:
                # DictReader usa la primera fila como nombres de campos
                lector = csv.DictReader(archivo)
                
                for fila in lector:
                    # Creamos la estructura con subdocumentos para que coincida con tu DB
                    nuevo_empleado = {
                        "nombre": fila.get("nombre"),
                        "direccion": {
                            "calle": fila.get("calle"),
                            "ciudad": fila.get("ciudad"),
                            "region": "Atacama"
                        },
                        "contacto": {
                            "telefono": fila.get("telefono"),
                            "correo": fila.get("correo")
                        },
                        "fecha_inicio": datetime.now(), # O procesar fila.get("fecha")
                        "salario": float(fila.get("salario", 0)),
                        "departamento": fila.get("departamento"),
                        "estado": "activo"
                    }
                    empleados_a_importar.append(nuevo_empleado)

            # C. Inserción masiva en MongoDB
            if empleados_a_importar:
                resultado = self.modelo_empleado.importar_masivo(empleados_a_importar)
                total = len(resultado.inserted_ids)
                QMessageBox.information(self, "Éxito", f"Se han importado {total} empleados.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo procesar el archivo:\n{e}")
