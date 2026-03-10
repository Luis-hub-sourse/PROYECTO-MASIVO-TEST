import sys
from PyQt5 import QtWidgets, uic
from ventanas.ventana_alumnos import VentanaAlumnos
from ventanas.ventana_profesores import VentanaProfesores
from ventanas.ventana_usuarios import VentanaUsuarios
from ventanas.ventana_inasistencia import VentanaRegsitroInasistencia
from ventanas.ventana_materias import VentanaMaterias

class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("xml/ventana_principal.ui", self)
        self.actionSalir.triggered.connect(QtWidgets.qApp.quit)
        self.btnSalir.clicked.connect(QtWidgets.qApp.quit)
        self.actionProfesores.triggered.connect(self.abrir_profesores)
        self.btnProfesores.clicked.connect(self.abrir_profesores)
        self.actionAlumnos.triggered.connect(self.abrir_alumnos)
        self.btnAlumnos.clicked.connect(self.abrir_alumnos)
        self.actionMaterias.triggered.connect(self.abrir_materias)
        self.btnMaterias.clicked.connect(self.abrir_materias)
        self.actionUsuarios.triggered.connect(self.abrir_usuarios)
        self.btnUsuarios.clicked.connect(self.abrir_usuarios)
        self.actionAcercade.triggered.connect(self.mostrar_acercade)
        self.actionUsuarios_2.triggered.connect(self.sobre_usuarios)
        self.actionInasistencias.triggered.connect(self.abrir_inasistencias)
        self.btnInasistencias.clicked.connect(self.abrir_inasistencias)
    
    def abrir_profesores(self):
        self.ventana_profesores = VentanaProfesores(self)
        self.ventana_profesores.show()
    
    def abrir_alumnos(self):
        self.ventana_alumnos = VentanaAlumnos(self)
        self.ventana_alumnos.show()
    
    def abrir_materias(self):
        self.ventana_materias = VentanaMaterias()
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


def main():
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
