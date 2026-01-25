import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from servicios.servicio_materia import ServicioMateria


class VentanaMaterias(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/materias.ui", self)
        
        # Inicializar servicio
        self.servicio_materia = ServicioMateria()
        self.materia_editando = None
        
        # Conectar botones
        self.btnCerrar.clicked.connect(self.close)
        self.btnAgregar.clicked.connect(self.agregar_materia)
        self.btnEliminar.clicked.connect(self.eliminar_materia)
        self.btnModificar.clicked.connect(self.modificar_materia)
        self.tlbMaterias.itemSelectionChanged.connect(self.cargar_datos_seleccionados)
        
        # Configurar tabla
        self.tlbMaterias.setColumnWidth(0, 200)  # Nombre
        self.tlbMaterias.setColumnWidth(1, 200)  # Carrera
        self.tlbMaterias.setColumnWidth(2, 200)  # Año
        
        # Cargar datos iniciales
        self.listar_materias()
        
    def listar_materias(self):
        materias = self.servicio_materia.listar_materias()
        self.tlbMaterias.setRowCount(len(materias))
        
        for row, materia in enumerate(materias):
            self.tlbMaterias.setItem(row, 0, QTableWidgetItem(str(materia[0])))  # Nombre
            self.tlbMaterias.setItem(row, 1, QTableWidgetItem(str(materia[1])))  # Carrera
            self.tlbMaterias.setItem(row, 2, QTableWidgetItem(str(materia[2])))  # Año
    
    def agregar_materia(self):
        nombre = self.txtNombre.text().strip()
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
        nuevo_nombre = self.txtNombre.text().strip()
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
    
    def cargar_datos_seleccionados(self):
        fila = self.tlbMaterias.currentRow()
        if fila != -1:
            self.txtNombre.setText(self.tlbMaterias.item(fila, 0).text())
            self.txtCarrera.setText(self.tlbMaterias.item(fila, 1).text())
            self.txtAnio.setText(self.tlbMaterias.item(fila, 2).text())
            # Guardar el nombre original para la modificación
            self.materia_editando = self.tlbMaterias.item(fila, 0).text()
    
    def limpiar_formulario(self):
        self.txtNombre.clear()
        self.txtCarrera.clear()
        self.txtAnio.clear()
        self.materia_editando = None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaMaterias()
    ventana.show()
    sys.exit(app.exec_())
