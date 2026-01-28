import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from servicios.servicio_materia import ServicioMateria
from servicios.servicio_carrera import ServicioCarrera


class VentanaMaterias(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/materias.ui", self)
        
        # Inicializar servicio
        self.servicio_materia = ServicioMateria()
        self.servicio_carrera = ServicioCarrera()
        self.materia_editando = None
        
        # Conectar botones de materias
        self.btnCerrar.clicked.connect(self.close)
        self.btnAgregar.clicked.connect(self.agregar_materia)
        self.btnEliminar.clicked.connect(self.eliminar_materia)
        self.btnModificar.clicked.connect(self.modificar_materia)
        self.tlbMaterias.itemSelectionChanged.connect(self.cargar_datos_seleccionados_materias)

        # Conetar botones de carreras
        self.btnAgregar_2.clicked.connect(self.agregar_carrera)
        self.btnModificar_2.clicked.connect(self.modificar_carrera)
        self.btnEliminar_2.clicked.connect(self.eliminar_carrera)
        self.tlbCarreras.itemSelectionChanged.connect(self.cargar_datos_seleccionados_carreras)

        # Configurar tabla Materias
        self.tlbMaterias.setColumnWidth(0, 200)  # Nombre
        self.tlbMaterias.setColumnWidth(1, 200)  # Carrera
        self.tlbMaterias.setColumnWidth(2, 200)  # Año

        # Configurar tabla Carreras
        self.tlbCarreras.setColumnWidth(0, 481) # Nombre
        
        # Cargar datos iniciales
        self.listar_materias()
        self.listar_carreras()
        
    def listar_materias(self):
        materias = self.servicio_materia.listar_materias()
        self.tlbMaterias.setRowCount(len(materias))
        
        for row, materia in enumerate(materias):
            self.tlbMaterias.setItem(row, 0, QTableWidgetItem(str(materia[0])))  # Nombre
            self.tlbMaterias.setItem(row, 1, QTableWidgetItem(str(materia[1])))  # Carrera
            self.tlbMaterias.setItem(row, 2, QTableWidgetItem(str(materia[2])))  # Año
    
    def agregar_materia(self):
        nombre = self.txtNombre_1.text().strip()
        carrera = self.txtCarrera.text().strip()
        anio = self.txtAnio.text().strip()
        
        if not nombre or not carrera or not anio:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return
        
        exito, mensaje = self.servicio_materia.agregar_materia(nombre, carrera, anio)
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.listar_materias()
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    def eliminar_materia(self):
        fila_seleccionada = self.tlbMaterias.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una materia para eliminar.")
            return
        
        nombre = self.tlbMaterias.item(fila_seleccionada, 0).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar la materia {nombre}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            exito, mensaje = self.servicio_materia.eliminar_materia(nombre)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.listar_materias()
                self.limpiar_formulario()
            else:
                QMessageBox.critical(self, "Error", mensaje)
    
    def modificar_materia(self):
        fila_seleccionada = self.tlbMaterias.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una materia para modificar.")
            return
        
        # Nombre original para buscar la materia
        nombre_original = self.materia_editando if self.materia_editando else self.tlbMaterias.item(fila_seleccionada, 0).text()
        
        # Nuevos valores desde los campos de texto
        nuevo_nombre = self.txtNombre_1.text().strip()
        nueva_carrera = self.txtCarrera.text().strip()
        nuevo_anio = self.txtAnio.text().strip()
        
        if not nuevo_nombre or not nueva_carrera or not nuevo_anio:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return
        
        exito, mensaje = self.servicio_materia.modificar_materia(nombre_original, nuevo_nombre, nueva_carrera, nuevo_anio)
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.listar_materias()
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    def cargar_datos_seleccionados_materias(self):
        fila = self.tlbMaterias.currentRow()
        if fila != -1:
            self.txtNombre_1.setText(self.tlbMaterias.item(fila, 0).text())
            self.txtCarrera.setText(self.tlbMaterias.item(fila, 1).text())
            self.txtAnio.setText(self.tlbMaterias.item(fila, 2).text())
            # Guardar el nombre original para la modificación
            self.materia_editando = self.tlbMaterias.item(fila, 0).text()

    def cargar_datos_seleccionados_carreras(self):
        fila = self.tlbCarreras.currentRow()
        if fila != -1:
            self.txtCarrera.setText(self.tlbCarreras.item(fila, 0).text())
            self.txtNombre_2.setText(self.tlbCarreras.item(fila, 0).text())
    
    def limpiar_formulario(self):
        self.txtNombre_1.clear()
        self.txtCarrera.clear()
        self.txtAnio.clear()
        self.txtNombre_2.clear()
        self.materia_editando = None

    def listar_carreras(self):
        carreras = self.servicio_carrera.listar_carreras()
        self.tlbCarreras.setRowCount(len(carreras))
        
        for row, carrera in enumerate(carreras):
            self.tlbCarreras.setItem(row, 0, QTableWidgetItem(str(carrera[0])))  # Nombre    

    def agregar_carrera(self):
        nombre = self.txtNombre_2.text().strip()
        
        if not nombre:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return
        
        exito, mensaje = self.servicio_carrera.agregar_carrera(nombre)
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.listar_carreras()
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", mensaje)

    def modificar_carrera(self):
        fila_seleccionada = self.tlbCarreras.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una carrera para modificar.")
            return
        
        # Nombre original para buscar la materia
        nombre_original = self.tlbCarreras.item(fila_seleccionada, 0).text()
        
        # Nuevos valores desde los campos de texto
        nuevo_nombre = self.txtNombre_2.text().strip()
        
        if not nuevo_nombre:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return
        
        exito, mensaje = self.servicio_carrera.modificar_carrera(nombre_original, nuevo_nombre)
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.listar_carreras()
            self.listar_materias()  # Actualizar materias en caso de que la carrera haya cambiado
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", mensaje)

    def eliminar_carrera(self):
        fila_seleccionada = self.tlbCarreras.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una carrera para eliminar.")
            return
        
        nombre = self.tlbCarreras.item(fila_seleccionada, 0).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar la carrera {nombre}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            exito, mensaje = self.servicio_carrera.eliminar_carrera(nombre)
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.listar_carreras()
                self.listar_materias() # Actualizar materias en caso de que la carrera haya sido eliminada
                self.limpiar_formulario()
            else:
                QMessageBox.critical(self, "Error", mensaje)