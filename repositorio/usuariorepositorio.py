from db.connexion_posgreSQL import ConexionDB

class UsuarioRepositorio:
    def __init__(self):
        self.db = ConexionDB()

    def agregar_usuario(self, usuario):
        consulta = "INSERT INTO usuarios (correo_electronico, contrasena, rol) VALUES (%s, %s, %s);"
        datos = (usuario.correo_electronico, usuario.contraseña, usuario.rol)
        return self.db.ejecutar_consulta(consulta, datos)

    def obtener_usuario(self):
        consulta = "SELECT * FROM usuarios;"
        usuarios = self.db.obtencion(consulta, ())
        return usuarios

    def eliminar_usuario(self, id):
        consulta = "DELETE FROM usuarios WHERE id_usuario = %s;"
        dato = (id,)
        return self.db.ejecutar_consulta(consulta, dato)
    
    def buscar_id(self, correo, contraseña, rol):
        consulta = "SELECT id_usuario FROM usuarios WHERE correo_electronico = %s AND contrasena = %s AND rol = %s;"
        datos = (correo, contraseña, rol)
        result = self.db.obtencion(consulta, datos)
        return result[0] if result else None
    
    def modificar_usuario(self, id, nuevo_correo, nueva_contraseña, nuevo_rol):
        consulta = "UPDATE usuarios SET correo_electronico = %s, contrasena = %s, rol = %s WHERE id_usuario = %s;"
        datos = (nuevo_correo, nueva_contraseña, nuevo_rol, id)
        return self.db.ejecutar_consulta(consulta, datos)