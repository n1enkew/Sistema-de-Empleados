from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
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

        self.ui.cbx_seleccionar_empleado.currentIndexChanged.connect(self.cargar_datos_en_campos)

        self.ui.btn_registrar.clicked.connect(self.sec_registrar_empleado)
        self.ui.btn_modificar_eliminar.clicked.connect(self.sec_modificar_eliminar_empleado)
        self.ui.btn_mostrar.clicked.connect(self.sec_mostrar_empleados)

        self.ui.btn_guardar_empleado.clicked.connect(self.registrar_empleado)

        self.ui.btn_guardar_mod.clicked.connect(self.modificar_empleado)
        self.ui.btn_eliminar_empleado.clicked.connect(self.eliminar_empleado)

        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0)) # Para que se abra en la seccion de registrar empleado por defecto

    def sec_registrar_empleado(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0))
        print("Registrar empleado")

    def sec_modificar_eliminar_empleado(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(1))
        self.cargar_nombres_combobox() # Cargar los nombres de empleados en el ComboBox
        print("Modificar/Eliminar empleado")

    def sec_mostrar_empleados(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(2))
        print("Mostrar empleados")

    def cargar_nombres_combobox(self):
        self.ui.cbx_seleccionar_empleado.clear()
        # Obtenemos la lista de la base de datos
        empleados = self.modelo_empleado.consultar_empleados()
        for emp in empleados:
            self.ui.cbx_seleccionar_empleado.addItem(emp["nombre"])

    def cargar_datos_en_campos(self):
        nombre_sel = self.ui.cbx_seleccionar_empleado.currentText()
        
        # Si el combobox está vacío (por ejemplo, después de un .clear()), no hacemos nada
        if not nombre_sel or nombre_sel == "": 
            return
        
        try:
            # Buscamos en la base de datos
            empleado = self.modelo_empleado.coleccion.find_one({"nombre": nombre_sel})
            
            if empleado:
                # Usamos .get() para evitar errores si una llave no existe
                self.ui.m_nombre.setText(empleado.get("nombre", ""))
                
                # Acceso a subdocumentos (Dirección)
                direccion = empleado.get("direccion", {})
                self.ui.m_calle.setText(direccion.get("calle", ""))
                self.ui.m_ciudad.setText(direccion.get("ciudad", ""))
                
                # Acceso a subdocumentos (Contacto)
                contacto = empleado.get("contacto", {})
                self.ui.m_telefono.setText(contacto.get("telefono", ""))
                self.ui.m_correo.setText(contacto.get("correo", ""))
                
                # Cargar salario (convertir a string para el QLineEdit)
                self.ui.m_salario.setText(str(empleado.get("salario", 0)))
                
                # Cargar fecha (si se guardó como datetime)
                fecha = empleado.get("fecha_inicio")
                if isinstance(fecha, datetime):
                    self.ui.m_fecha_inicio.setDate(QDate(fecha.year, fecha.month, fecha.day))
                
                # Cargar Departamento en el ComboBox de modificación
                # Reemplaza 'm_dpto_asig' por el nombre real de tu combobox en la pestaña de mod
                #idx = self.ui.m_dpto_asig.findText(empleado.get("departamento", ""))
                #if idx >= 0:
                #    self.ui.m_dpto_asig.setCurrentIndex(idx)
                    
        except Exception as e:
            print(f"Error al cargar datos del empleado: {e}")

    def eliminar_empleado(self):
            nombre = self.ui.cbx_seleccionar_empleado.currentText().strip()
            
            if not nombre: return

            msg = QMessageBox.question(self, "Confirmar", f"¿Eliminar a {nombre}?", 
                                    QMessageBox.Yes | QMessageBox.No)
            
            if msg == QMessageBox.Yes:
                resultado = self.modelo_empleado.eliminar_empleado(nombre)
                
                # VERIFICACIÓN REAL
                if resultado.deleted_count > 0:
                    print(f"Éxito: {nombre} fue eliminado de la base de datos.")
                    self.cargar_nombres_combobox()
                    # Limpiar campos después de borrar
                    self.ui.m_nombre.clear()
                    self.ui.m_calle.clear()
                    # ... resto de clears
                else:
                    print("Error: No se encontró el registro en MongoDB para eliminar.")

    def modificar_empleado(self):
        # Usamos .strip() para evitar espacios invisibles al inicio o final
        nombre_original = self.ui.cbx_seleccionar_empleado.currentText().strip()
        
        if not nombre_original:
            print("Error: No se ha seleccionado un empleado.")
            return

        datos_actualizados = {
            "nombre": self.ui.m_nombre.text().strip(),
            "direccion": {
                "calle": self.ui.m_calle.text(),
                "ciudad": self.ui.m_ciudad.text(),
                "region": "Atacama"
            },
            "contacto": {
                "telefono": self.ui.m_telefono.text(),
                "correo": self.ui.m_correo.text()
            },
            "salario": float(self.ui.m_salario.text() or 0)
        }
        
        resultado = self.modelo_empleado.actualizar_empleado(nombre_original, datos_actualizados)
        
        # VERIFICACIÓN REAL
        if resultado.modified_count > 0:
            print(f"Éxito: Se actualizaron los datos de {nombre_original}.")
            self.cargar_nombres_combobox() # Refrescar la lista por si cambió el nombre
        else:
            print("Aviso: No se realizaron cambios (el nombre no coincide o los datos son iguales).")

    def registrar_empleado(self):
        try:
            nombre = self.ui.r_nombre.text()
            calle = self.ui.r_calle.text()
            ciudad = self.ui.r_ciudad.text()

            if not nombre:
                print("El nombre es obligatorio")
                return

            fecha_qdate = self.ui.r_fecha_inicio.date()
            fecha_dt = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())
             
            datos_direccion = {
            "calle": calle,
            "ciudad": ciudad,
            "region": "Atacama"
            }

            self.modelo_empleado.crear_empleado(
                nombre, 
                datos_direccion, 
                self.ui.r_telefono.text(),
                self.ui.r_correo.text(),
                fecha_dt,
                float(self.ui.r_salario.text() or 0),
                self.ui.r_dpto_asig.currentText() # Si usas un ComboBox para el depto
            )
            
            print(f"Empleado {nombre} registrado exitosamente en MongoDB.")
            self.limpiar_formulario()
        
        except Exception as e:
            print(f"Error al registrar: {e}")

    def limpiar_formulario(self):
        # Es buena práctica limpiar los campos después de guardar
            self.ui.r_nombre.clear()
            self.ui.r_calle.clear()
            self.ui.r_ciudad.clear()
            self.ui.r_telefono.clear()
            self.ui.r_correo.clear()
            self.ui.r_salario.clear()
            self.ui.r_fecha_inicio.setDate(QDate.currentDate())
        