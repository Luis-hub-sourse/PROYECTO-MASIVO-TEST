from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu
from servicios.usuarioservicio import UsuarioServicio

class VentanaUsuarios(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("xml/usuarios.ui", self)
        self.servicio_usuario = UsuarioServicio()
        
        self.btnIngresar.clicked.connect(self.ingresar_usuario)
        self.btnModificar.clicked.connect(self.modificar_usuario)
        self.btnMas.clicked.connect(lambda: (self.limpiar_campos(), self.LineNombre.setFocus()))
        self.btnCancelar.clicked.connect(self.limpiar_campos)
        self.LineNombre.returnPressed.connect(self.LineContrasena.setFocus)

        self.tlbUsuarios.cellClicked.connect(self.seleccion)
        self.tlbUsuarios.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tlbUsuarios.customContextMenuRequested.connect(self.menu_contextual)

        self.listar_usuarios()

    # Menu desplegable al hacer click derecho en una de las filas de la tabla
    def menu_contextual(self, pos):
        try:
            row = self.tlbUsuarios.rowAt(pos.y())
            if row >= 0:
                nombre, contraseña = self.tlbUsuarios.item(row, 0).text(), self.tlbUsuarios.item(row, 1).text()
                menu = QMenu()
                eliminar = menu.addAction("Eliminar fila")
                #modificar = menu.addAction("Modificar fila")                
                accion = menu.exec(self.tlbUsuarios.mapToGlobal(pos))
            
            #if accion == modificar:
            if accion == eliminar:
                respuesta = self.mensaje_confirmacion("¿Está seguro que desea eliminar este elemento?")

                if respuesta:
                    self.tlbUsuarios.removeRow(row)
                    if self.servicio_usuario.eliminar_usuario(nombre, contraseña):
                        self.mensaje_aviso(f"Usuario {nombre} eliminado exitosamente.")
                        self.listar_usuarios()
                    else:
                        self.mensaje_aviso_error(f"No se pudo eliminar el usaurio {nombre} selecionado.")
                else:
                    self.mensaje_aviso("Eliminación cancelada.")
        except Exception as e:
            self.mensaje_aviso_error(f"Error al procesar la acción del menú contextual: {e}")

    def listar_usuarios(self):
        try:
            usuarios = self.servicio_usuario.obtener_todos_los_usuarios()
            
            if usuarios is False:
                self.mensaje_aviso_error("No hay usuarios registrados.")
            else:
                print("\nLista de usuarios")
                self.tlbUsuarios.setRowCount(len(usuarios))
                self.tlbUsuarios.setColumnCount(2)
                for row, usuario in enumerate(usuarios):
                    self.tlbUsuarios.setItem(row, 0, QtWidgets.QTableWidgetItem(str(usuario[1])))
                    self.tlbUsuarios.setItem(row, 1, QtWidgets.QTableWidgetItem(str(usuario[2])))
        except Exception as ex:
            self.mensaje_aviso_error(ex)

    def ingresar_usuario(self):
        try:
            nombre = self.LineNombre.text()
            contraseña = self.LineContrasena.text()

            if not nombre or not contraseña:
                self.mensaje_aviso_error("Por favor, complete todos los campos.")
            else:
                if self.servicio_usuario.agregar_usuario(nombre, contraseña):
                    self.mensaje_aviso(f"Usuario {nombre} agregado exitosamente.")
                    self.listar_usuarios()
                else:
                    self.mensaje_aviso_error("Se produjo un error al ingresar el usaurio, intenetelo nuevamente.")
        except Exception as ex:
            self.mensaje_aviso_error(ex)

    def seleccion(self):
        try:
            row = self.tlbUsuarios.currentRow()
            self.nombre_actual = self.tlbUsuarios.item(row, 0).text()
            self.contraseña_actual = self.tlbUsuarios.item(row, 1).text()

            self.LineNombre.setText(self.nombre_actual)
            self.LineContrasena.setText(self.contraseña_actual)
            self.LineNombre.setFocus()
            self.LineNombre.returnPressed.connect(self.LineContrasena.setFocus)
        except Exception as ex:
            self.mensaje_aviso_error(f"Error al seleccionar el usuario: {ex}")
    
    def modificar_usuario(self):
        try:
            nuevo_nombre = self.LineNombre.text()
            nuevo_contraseña = self.LineContrasena.text()

            respuesta = self.mensaje_confirmacion("¿Está seguro que desea modificar este elemento?")

            if respuesta and self.nombre_actual and self.contraseña_actual and nuevo_nombre and nuevo_contraseña:
                if self.servicio_usuario.modificar_usuario(self.nombre_actual, self.contraseña_actual, nuevo_nombre, nuevo_contraseña):
                    self.mensaje_aviso(f"Usuario {self.nombre_actual} modificado exitosamente.")
                    self.listar_usuarios()
                else:
                    self.mensaje_aviso_error(f"No se pudo modificar el usaurio {self.nombre_actual} selecionado.")
            else:
                self.mensaje_aviso_error("Modificación cancelada.")
        except Exception as e:
            self.mensaje_aviso_error(f"Error al modificar el usuario: {e}")

    def limpiar_campos(self):
        self.LineNombre.clear()
        self.LineContrasena.clear()

    # Ventana de aviso con mensajes de error
    def mensaje_aviso_error(self, mensaje):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setText(mensaje)
        msg_box.setWindowTitle("Aviso")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec()

    # Ventana de aviso con mensajes de información
    def mensaje_aviso(self, mensaje):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setText(mensaje)
        msg_box.setWindowTitle("Aviso")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec()
    
    def mensaje_confirmacion(self, mensaje):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Question)
        msg_box.setText(mensaje)
        msg_box.setWindowTitle("Confirmación")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        return msg_box.exec() == QtWidgets.QMessageBox.Yes
