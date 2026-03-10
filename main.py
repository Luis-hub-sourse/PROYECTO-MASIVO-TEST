import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from servicios.servicio_materia import ServicioMateria
from ventanas.ventana_alumnos import VentanaAlumnos
from ventanas.ventana_profesores import VentanaProfesores
from ventanas.ventana_usuarios import VentanaUsuarios
from ventanas.ventana_inasistencia import VentanaRegsitroInasistencia

class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("xml/ventana_principal.ui", self)
        self.actionSalir.triggered.connect(QtWidgets.qApp.quit)
        self.actionProfesores.triggered.connect(self.abrir_profesores)
        self.actionAlumnos.triggered.connect(self.abrir_alumnos)
        self.actionMaterias.triggered.connect(self.abrir_materias)
        self.actionUsuarios.triggered.connect(self.abrir_usuarios)
        self.actionAcercade.triggered.connect(self.mostrar_acercade)
        self.actionUsuarios_2.triggered.connect(self.sobre_usuarios)
        self.actionInasistencias.triggered.connect(self.abrir_inasistencias)
    
    def abrir_profesores(self):
        self.ventana_profesores = VentanaProfesores(self)
        self.ventana_profesores.show()
    
    def abrir_alumnos(self):
        self.ventana_alumnos = VentanaAlumnos(self)
        self.ventana_alumnos.show()
    
    def abrir_materias(self):
        self.ventana_materias = VentanaMaterias(self)
        self.ventana_materias.show()
    
    def abrir_usuarios(self):
        self.ventana_usuarios = VentanaUsuarios()
        self.ventana_usuarios.show()

    def abrir_inasistencias(self):
        self.ventana_inasistencias = VentanaRegsitroInasistencia(self)
        self.ventana_inasistencias.show()

    def mostrar_acercade(self):
        QtWidgets.QMessageBox.information(self, "Acerca de", "Aplicación de Gestión de Asistencias para alumnos y profesores.\nDesarrollada por los alumnos de 2do año del ITES.")
    
    def sobre_usuarios(self):
        QtWidgets.QMessageBox.information(self, "Sobre Usuarios", "En este sistema puedes gestionar los usuarios.\nPuedes agregar, eliminar o modificar usuarios existentes.")



class VentanaMaterias(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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


def main():
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
