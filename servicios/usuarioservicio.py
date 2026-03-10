from entidades.usuarios import Usuarios
from repositorio.usuariorepositorio import UsuarioRepositorio
from gestion.gestionusuarios import Verificacion

class UsuarioServicio:
    def __init__(self):
        self.repositorio = UsuarioRepositorio()

    def obtener_todos_los_usuarios(self): 
        usuarios = self.repositorio.obtener_usuario()
        if usuarios is not None:
            return usuarios
        else:
            return False
    
    def agregar_usuario(self, nombre, contraseña):
        if not self.verificar_datos(nombre, contraseña):
            return False
        else:
            usuario = Usuarios(nombre, contraseña)
            return self.repositorio.agregar_usuario(usuario)

    def eliminar_usuario(self, nombre, contraseña):
        id = self.repositorio.buscar_id(nombre, contraseña)
        if id is not None:
            return self.repositorio.eliminar_usuario(id)
        return False

    def modificar_usuario(self, nombre_actual, contraseña_actual, nuevo_nombre, nueva_contraseña):
        id = self.repositorio.buscar_id(nombre_actual, contraseña_actual)
        if id is not None:
            if self.verificar_datos(nuevo_nombre, nueva_contraseña):
                return self.repositorio.modificar_usuario(id, nuevo_nombre, nueva_contraseña)
            return False
        return False
    
    def verificar_datos(self, nombre, contraseña):
        verificacion = Verificacion(nombre, contraseña)
        return verificacion.verificar_tamaño()