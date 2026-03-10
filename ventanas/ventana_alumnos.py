from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from servicios.servicio_alumno import ServicioAlumno


class VentanaAlumnos(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/alumnos.ui", self)
        
        # Inicializar servicio
        self.servicio_alumno = ServicioAlumno()
        self.alumno_editando = None
        
        # Conectar botones
        self.btnCerrar.clicked.connect(self.close)
        self.btnAgregar.clicked.connect(self.agregar_alumno)
        self.btnEditar.clicked.connect(self.editar_alumno)
        self.btnEliminar.clicked.connect(self.eliminar_alumno)
        self.btnGuardar.clicked.connect(self.guardar_alumno)
        self.btnCancelar.clicked.connect(self.cancelar_edicion)

        self.tlbAlumnos.setColumnWidth(3, 250) # Ajustar ancho de la columna de correo
        self.tlbAlumnos.setColumnWidth(5, 240) # Ajustar ancho de la columna de ciudad

        self.txtDni.setMaxLength(10)  # Limitar el número de caracteres del DNI

        self.txtDni.returnPressed.connect(self.txtNombre.setFocus)
        self.txtNombre.returnPressed.connect(self.txtApellido.setFocus)
        self.txtApellido.returnPressed.connect(self.txtCorreo.setFocus)
        self.txtCorreo.returnPressed.connect(self.txtTelefono.setFocus)
        self.txtTelefono.returnPressed.connect(self.txtCiudad.setFocus)
        self.txtCiudad.returnPressed.connect(self.btnGuardar.click)
        
        # Cargar datos iniciales
        self.listar_alumnos()
        
    def listar_alumnos(self):
        alumnos = self.servicio_alumno.listar_alumnos()
        self.tlbAlumnos.setRowCount(len(alumnos))
        
        for row, alumno in enumerate(alumnos):
            self.tlbAlumnos.setItem(row, 0, QTableWidgetItem(str(alumno[0])))  # Dni
            self.tlbAlumnos.setItem(row, 1, QTableWidgetItem(str(alumno[1])))  # Nombre
            self.tlbAlumnos.setItem(row, 2, QTableWidgetItem(str(alumno[4])))  # Apellido
            self.tlbAlumnos.setItem(row, 3, QTableWidgetItem(str(alumno[3])))  # Correo
            self.tlbAlumnos.setItem(row, 4, QTableWidgetItem(str(alumno[5])))  # Teléfono
            self.tlbAlumnos.setItem(row, 5, QTableWidgetItem(str(alumno[2])))  # Ciudad

    def agregar_alumno(self):
        self.limpiar_formulario()
        self.tabWidget.setCurrentIndex(1)  # Cambiar a la pestaña del formulario
        self.alumno_editando = None
    
    def editar_alumno(self):
        fila_seleccionada = self.tlbAlumnos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un alumno para editar.")
            return
        
        nombre_actual = self.tlbAlumnos.item(fila_seleccionada, 1).text()
        alumno = self.servicio_alumno.buscar_alumno(nombre_actual)
        
        if alumno:
            self.txtDni.setText(str(alumno[0]))
            self.txtNombre.setText(str(alumno[1]))
            self.txtApellido.setText(str(alumno[4]))
            self.txtCorreo.setText(str(alumno[3]))
            self.txtTelefono.setText(str(alumno[5]))
            self.txtCiudad.setText(str(alumno[2]))
            
            self.tabWidget.setCurrentIndex(1)
            self.alumno_editando = alumno[0]
    
    def eliminar_alumno(self):
        fila_seleccionada = self.tlbAlumnos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un alumno para eliminar.")
            return
        
        dni = self.tlbAlumnos.item(fila_seleccionada, 0).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar al alumno {dni}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            exito, mensaje = self.servicio_alumno.eliminar_alumno(dni)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.listar_alumnos()
            else:
                QMessageBox.critical(self, "Error", mensaje)
    
    def guardar_alumno(self):
        dni = self.txtDni.text().strip()
        nombre = self.txtNombre.text().strip()
        apellido = self.txtApellido.text().strip()
        correo = self.txtCorreo.text().strip()
        telefono = self.txtTelefono.text().strip()
        ciudad = self.txtCiudad.text().strip()
        
        if self.alumno_editando:
            # Modo edición
            exito, mensaje = self.servicio_alumno.actualizar_alumno(
                self.alumno_editando, dni, nombre, apellido, correo, telefono, ciudad
            )
        else:
            # Modo agregar
            exito, mensaje = self.servicio_alumno.agregar_alumno(
                dni, nombre, apellido, correo, telefono, ciudad
            )
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.listar_alumnos()
            self.tabWidget.setCurrentIndex(0)  # Volver a la lista
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    def cancelar_edicion(self):
        self.limpiar_formulario()
        self.tabWidget.setCurrentIndex(0)
    
    def limpiar_formulario(self):
        self.txtDni.clear()
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtCorreo.clear()
        self.txtTelefono.clear()
        self.txtCiudad.clear()
        self.alumno_editando = None


