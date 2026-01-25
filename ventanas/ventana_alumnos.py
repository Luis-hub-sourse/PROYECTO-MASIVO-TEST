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
        
        # Configurar tabla
        self.tlbAlumnos.setColumnWidth(0, 250)  # Nombre
        self.tlbAlumnos.setColumnWidth(1, 250)  # Carrera
        self.tlbAlumnos.setColumnWidth(2, 100)  # Año
        
        # Cargar datos iniciales
        self.listar_alumnos()
        
    def listar_alumnos(self):
        alumnos = self.servicio_alumno.listar_alumnos()
        self.tlbAlumnos.setRowCount(len(alumnos))
        
        for row, alumno in enumerate(alumnos):
            self.tlbAlumnos.setItem(row, 0, QTableWidgetItem(str(alumno[0])))  # Nombre
            self.tlbAlumnos.setItem(row, 1, QTableWidgetItem(str(alumno[1])))  # Carrera
            self.tlbAlumnos.setItem(row, 2, QTableWidgetItem(str(alumno[2])))  # Año
    
    def agregar_alumno(self):
        self.limpiar_formulario()
        self.tabWidget.setCurrentIndex(1)  # Cambiar a la pestaña del formulario
        self.alumno_editando = None
    
    def editar_alumno(self):
        fila_seleccionada = self.tlbAlumnos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un alumno para editar.")
            return
        
        nombre_actual = self.tlbAlumnos.item(fila_seleccionada, 0).text()
        alumno = self.servicio_alumno.buscar_alumno(nombre_actual)
        
        if alumno:
            self.txtNombre.setText(str(alumno[0]))
            self.txtCarrera.setText(str(alumno[1]))
            self.txtAnio.setText(str(alumno[2]))
            
            self.txtNombre.setEnabled(False)  # No permitir cambiar el nombre
            self.tabWidget.setCurrentIndex(1)
            self.alumno_editando = alumno[0]
    
    def eliminar_alumno(self):
        fila_seleccionada = self.tlbAlumnos.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un alumno para eliminar.")
            return
        
        nombre = self.tlbAlumnos.item(fila_seleccionada, 0).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar al alumno {nombre}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            exito, mensaje = self.servicio_alumno.eliminar_alumno(nombre)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.listar_alumnos()
            else:
                QMessageBox.critical(self, "Error", mensaje)
    
    def guardar_alumno(self):
        nombre = self.txtNombre.text().strip()
        carrera = self.txtCarrera.text().strip()
        anio = self.txtAnio.text().strip()
        
        if self.alumno_editando:
            # Modo edición
            exito, mensaje = self.servicio_alumno.actualizar_alumno(
                self.alumno_editando, nombre, carrera, anio
            )
        else:
            # Modo agregar
            exito, mensaje = self.servicio_alumno.agregar_alumno(
                nombre, carrera, anio
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
        self.txtNombre.clear()
        self.txtCarrera.clear()
        self.txtAnio.clear()
        self.txtNombre.setEnabled(True)
        self.alumno_editando = None


