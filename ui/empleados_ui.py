from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
from PySide6.QtGui import *
from datetime import datetime
from database.EmpleadoModel import EmpleadoModel



class Empleados_ui(QWidget):
    def __init__(self):
        super().__init__()
        self.EmpleadoModel = EmpleadoModel()
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

        self.cargar_departamentos_en_combo()

        self.ui.btn_registrar.clicked.connect(self.registrar_empleado)
        self.ui.btn_modificar_eliminar.clicked.connect(self.modificar_eliminar_empleado)
        self.ui.btn_mostrar.clicked.connect(self.mostrar_empleados)
        
        self.ui.btn_guardar_empleado.clicked.connect(self.guardar_empleado)
        self.ui.btn_eliminar_mod.clicked.connect(self.ejecutar_eliminacion)

        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0)) # Para que se abra en la seccion de registrar empleado por defecto

        self.ui.cbx_seleccionar_empleado.currentIndexChanged.connect(self.cargar_datos_empleado_mod)
        self.ui.btn_guardar_mod.clicked.connect(self.ejecutar_modificacion)

        

        self.modelo_tabla = QStandardItemModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.modelo_tabla)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.ui.tabla_empleados.setModel(self.proxy_model)

        self.ui.buscar_empleado.textChanged.connect(self.filtrar_tabla)

        self.aplicar_estilo_tabla()

    def registrar_empleado(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(0))
        print("Registrar empleado")

    def modificar_eliminar_empleado(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(1))
        print("Modificar/Eliminar empleado")

    def mostrar_empleados(self):
        self.ui.stack_empleado.setCurrentWidget(self.ui.stack_empleado.widget(2))
        print("Mostrar empleados")

    def guardar_empleado(self):
        try:
            nombre = self.ui.r_nombre.text()
            
            direccion = self.ui.r_direccion.text()
            telefono = self.ui.r_telefono.text()
            correo = self.ui.r_correo.text()
            
            fecha_qdate = self.ui.r_fecha_inicio.date()
            fecha_dt = datetime(fecha_qdate.year(), fecha_qdate.month(), fecha_qdate.day())
            salario_texto = self.ui.r_salario.text()
            salario_final = float(salario_texto) if salario_texto else 0.0

            # IMPORTANTE: Aquí deberías pasar el ID del depto, no el nombre.
            # Por ahora pasaremos 1 como prueba o el index del combobox
            id_depto = self.ui.r_dpto_asig.currentData()

            if id_depto is None:
                print("Error: Debe seleccionar un departamento válido.")
                return
            
            exito = self.EmpleadoModel.crear_empleado(
                nombre, 
                direccion,
                telefono,
                correo,
                fecha_dt,
                salario_final,
                id_depto
            )
            
            if exito:
                print(f"Empleado {nombre} guardado en MySQL.")
                self.limpiar_formulario()
        
        except Exception as e:
            print(f"Error en la interfaz: {e}")

    def limpiar_formulario(self):
    # 6. IMPLEMENTAR LIMPIEZA
        self.ui.r_nombre.clear()
        self.ui.r_direccion.clear()
        self.ui.r_telefono.clear()
        self.ui.r_correo.clear()
        self.ui.r_salario.clear()
        self.ui.r_fecha_inicio.setDate(QDate.currentDate())
    
    def cargar_departamentos_en_combo(self):
        # 1. Consultas los deptos de la DB
        conexion = self.EmpleadoModel.db.obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT idDepartamento, nombre FROM Departamento")
            deptos = cursor.fetchall()
            
            self.ui.r_dpto_asig.clear()
            for d in deptos:
                # El truco: mostramos el nombre, pero guardamos el ID oculto
                self.ui.r_dpto_asig.addItem(d["nombre"], d["idDepartamento"])

            self.ui.m_dpto_asig.clear()
            for d in deptos:
                # El truco: mostramos el nombre, pero guardamos el ID oculto
                self.ui.m_dpto_asig.addItem(d["nombre"], d["idDepartamento"])
            
            cursor.close()
            conexion.close()

    def modificar_eliminar_empleado(self):
        # Al entrar a la pestaña 1, cargamos los nombres
        self.ui.stack_empleado.setCurrentIndex(1)
        self.cargar_nombres_combobox_mod()
        # También cargamos los departamentos en el combo de esa sección
        self.cargar_departamentos_en_combo()

    def cargar_nombres_combobox_mod(self):
        empleados = self.EmpleadoModel.consultar_todos_lista()
        self.ui.cbx_seleccionar_empleado.clear()
        for emp in empleados:
            # Mostramos nombre, guardamos ID
            self.ui.cbx_seleccionar_empleado.addItem(emp["nombre"], emp["idEmpleado"])

    def cargar_datos_empleado_mod(self):
        id_emp = self.ui.cbx_seleccionar_empleado.currentData()
        if id_emp is None: return

        empleado = self.EmpleadoModel.consultar_por_id(id_emp)
        if empleado:
            self.ui.m_nombre.setText(empleado["nombre"])
            self.ui.m_direccion.setText(empleado["direccion"])
            self.ui.m_telefono.setText(empleado["telefono"])
            self.ui.m_correo.setText(empleado["correo"])
            self.ui.m_salario.setText(str(empleado["salario"]))
            
            fecha = empleado["fecha_inicio"]
            if isinstance(fecha, datetime):
                self.ui.m_fecha_inicio.setDate(QDate(fecha.year, fecha.month, fecha.day))
            
            # Seleccionar el departamento correcto en el combo de modificación
            id_depto = empleado["Departamento_idDepartamento"]
            idx = self.ui.m_dpto_asig.findData(id_depto)
            if idx >= 0:
                self.ui.m_dpto_asig.setCurrentIndex(idx)

    def ejecutar_modificacion(self):
        try:
            id_emp = self.ui.cbx_seleccionar_empleado.currentData()
            if id_emp is None: return

            # Recolectar nuevos datos
            nombre = self.ui.m_nombre.text()
            direccion = self.ui.m_direccion.text()
            tel = self.ui.m_telefono.text()
            correo = self.ui.m_correo.text()
            salario = float(self.ui.m_salario.text() or 0)
            id_depto = self.ui.m_dpto_asig.currentData()
            
            qf = self.ui.m_fecha_inicio.date()
            fecha_dt = datetime(qf.year(), qf.month(), qf.day())

            exito = self.EmpleadoModel.actualizar_empleado(
                id_emp, nombre, direccion, tel, correo, fecha_dt, salario, id_depto
            )

            if exito:
                print("Empleado actualizado correctamente.")
                self.cargar_nombres_combobox_mod() # Refrescar nombres por si cambió
        except Exception as e:
            print(f"Error al modificar: {e}")

    

    def ejecutar_eliminacion(self):
        # 1. Obtener el ID del empleado seleccionado
        id_emp = self.ui.cbx_seleccionar_empleado.currentData()
        nombre_emp = self.ui.cbx_seleccionar_empleado.currentText()

        if id_emp is None:
            QMessageBox.warning(self, "Advertencia", "Seleccione un empleado para eliminar.")
            return

        # 2. Pedir confirmación (Buena práctica de Analista)
        confirmacion = QMessageBox.question(
            self, 
            "Confirmar Eliminación", 
            f"¿Estás seguro de que deseas eliminar a {nombre_emp}?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            exito = self.EmpleadoModel.eliminar_empleado(id_emp)
            if exito:
                QMessageBox.information(self, "Éxito", f"Empleado {nombre_emp} eliminado.")
                # 3. Limpiar y refrescar la lista
                self.limpiar_campos_modificacion()
                self.cargar_nombres_combobox_mod()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el empleado.")

    def limpiar_campos_modificacion(self):
        self.ui.m_nombre.clear()
        self.ui.m_direccion.clear()
        self.ui.m_telefono.clear()
        self.ui.m_correo.clear()
        self.ui.m_salario.clear()
        self.ui.m_fecha_inicio.setDate(QDate.currentDate())

    def mostrar_empleados(self):
        """Carga los datos desde MySQL a la tabla"""
        self.ui.stack_empleado.setCurrentIndex(2)
        
        datos = self.EmpleadoModel.consultar_para_tabla()
        self.modelo_tabla.clear()
        
        # Definir encabezados
        headers = ["ID", "Nombre", "Dirección", "Teléfono", "Correo", "Inicio", "Salario", "Depto"]
        self.modelo_tabla.setHorizontalHeaderLabels(headers)

        for fila in datos:
            items = [
                QStandardItem(str(fila["idEmpleado"])),
                QStandardItem(str(fila["nombre"])),
                QStandardItem(str(fila["direccion"])),
                QStandardItem(str(fila["telefono"])),
                QStandardItem(str(fila["correo"])),
                QStandardItem(str(fila["fecha_inicio"])),
                QStandardItem(f"$ {fila['salario']:,.2f}"),
                QStandardItem(str(fila["departamento"] or "Sin Asignar"))
            ]
            self.modelo_tabla.appendRow(items)
        
        # Ajustar columnas al contenido
        self.ui.tabla_empleados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def filtrar_tabla(self, texto):
        """Filtra por nombre (columna 1) en tiempo real"""
        self.proxy_model.setFilterKeyColumn(1) # Filtra por la columna 'Nombre'
        self.proxy_model.setFilterFixedString(texto)

    def aplicar_estilo_tabla(self):
        self.ui.tabla_empleados.setStyleSheet("""
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