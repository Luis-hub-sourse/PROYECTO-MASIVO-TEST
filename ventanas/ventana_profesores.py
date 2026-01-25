from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from servicios.servicio_profesor import ServicioProfesor


class VentanaProfesores(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/profesores.ui", self)
        
        # Inicializar servicio
        self.servicio_profesor = ServicioProfesor()
        self.profesor_editando = None
        
        # Conectar botones
        self.btnCerrar.clicked.connect(self.close)
        self.btnAgregar.clicked.connect(self.agregar_profesor)
        self.btnEditar.clicked.connect(self.editar_profesor)
        self.btnEliminar.clicked.connect(self.eliminar_profesor)
        self.btnGuardar.clicked.connect(self.guardar_profesor)
        self.btnCancelar.clicked.connect(self.cancelar_edicion)
        
        # Configurar tabla
        self.tlbProfesores.setColumnWidth(0, 100)  # DNI
        self.tlbProfesores.setColumnWidth(1, 150)  # Nombre
        self.tlbProfesores.setColumnWidth(2, 150)  # Apellido
        self.tlbProfesores.setColumnWidth(3, 200)  # Correo
        self.tlbProfesores.setColumnWidth(4, 120)  # Teléfono
        
        # Cargar datos iniciales
        self.listar_profesores()
        
    def listar_profesores(self):
        profesores = self.servicio_profesor.listar_profesores()
        self.tlbProfesores.setRowCount(len(profesores))
        
        for row, profesor in enumerate(profesores):
            self.tlbProfesores.setItem(row, 0, QTableWidgetItem(str(profesor[0])))  # DNI
            self.tlbProfesores.setItem(row, 1, QTableWidgetItem(str(profesor[1])))  # Nombre
            self.tlbProfesores.setItem(row, 2, QTableWidgetItem(str(profesor[2])))  # Apellido
            self.tlbProfesores.setItem(row, 3, QTableWidgetItem(str(profesor[3])))  # Correo
            self.tlbProfesores.setItem(row, 4, QTableWidgetItem(str(profesor[4])))  # Teléfono
    
    def agregar_profesor(self):
        self.limpiar_formulario()
        self.tabWidget.setCurrentIndex(1)  # Cambiar a la pestaña del formulario
        self.profesor_editando = None
    
    def editar_profesor(self):
        fila_seleccionada = self.tlbProfesores.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un profesor para editar.")
            return
        
        dni = self.tlbProfesores.item(fila_seleccionada, 0).text()
        profesor = self.servicio_profesor.buscar_profesor(dni)
        
        if profesor:
            self.txtDNI.setText(str(profesor[0]))
            self.txtNombre.setText(str(profesor[1]))
            self.txtApellido.setText(str(profesor[2]))
            self.txtCorreo.setText(str(profesor[3]))
            self.txtTelefono.setText(str(profesor[4]))
            
            self.txtDNI.setEnabled(False)  # No permitir cambiar el DNI
            self.tabWidget.setCurrentIndex(1)
            self.profesor_editando = profesor[0]
    
    def eliminar_profesor(self):
        fila_seleccionada = self.tlbProfesores.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un profesor para eliminar.")
            return
        
        dni = self.tlbProfesores.item(fila_seleccionada, 0).text()
        nombre = self.tlbProfesores.item(fila_seleccionada, 1).text()
        apellido = self.tlbProfesores.item(fila_seleccionada, 2).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar al profesor {nombre} {apellido}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            exito, mensaje = self.servicio_profesor.eliminar_profesor(dni)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.listar_profesores()
            else:
                QMessageBox.critical(self, "Error", mensaje)
    
    def guardar_profesor(self):
        dni = self.txtDNI.text().strip()
        nombre = self.txtNombre.text().strip()
        apellido = self.txtApellido.text().strip()
        correo = self.txtCorreo.text().strip()
        telefono = self.txtTelefono.text().strip()
        
        if self.profesor_editando:
            # Modo edición
            exito, mensaje = self.servicio_profesor.actualizar_profesor(
                dni, nombre, apellido, correo, telefono
            )
        else:
            # Modo agregar
            exito, mensaje = self.servicio_profesor.agregar_profesor(
                dni, nombre, apellido, correo, telefono
            )
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.listar_profesores()
            self.tabWidget.setCurrentIndex(0)  # Volver a la lista
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    def cancelar_edicion(self):
        self.limpiar_formulario()
        self.tabWidget.setCurrentIndex(0)
    
    def limpiar_formulario(self):
        self.txtDNI.clear()
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtCorreo.clear()
        self.txtTelefono.clear()
        self.txtDNI.setEnabled(True)
        self.profesor_editando = None


