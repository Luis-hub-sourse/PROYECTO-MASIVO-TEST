from db.connexion_posgreSQL import ConexionDB

class RepositorioCarrera:
    def __init__(self):
        self.db = ConexionDB()

    def listar_carreras(self):
        consulta = "SELECT nombre FROM carreras ORDER BY nombre;"
        carreras = self.db.obtencion(consulta, ())
        return carreras
    
    def obtener_id_carrera(self, nombre):
        consulta = "SELECT id_carrera FROM carreras WHERE nombre = %s;"
        datos = (nombre,)
        resultados = self.db.obtencion(consulta, datos)
        if resultados:
            return resultados[0]
        return None
    
    def agregar_carrera(self, nombre):
        consulta = "INSERT INTO carreras (nombre) VALUES (%s);"
        return self.db.ejecutar_consulta(consulta, (nombre,))
    
    def modificar_carrera(self, nombre_original, nuevo_nombre):
        id_carrera = self.obtener_id_carrera(nombre_original)
        if id_carrera is None:
            return False, "La carrera no existe."
        consulta = "UPDATE carreras SET nombre = %s WHERE id_carrera = %s;"
        return self.db.ejecutar_consulta(consulta, (nuevo_nombre, id_carrera))
    
    def eliminar_carrera(self, nombre):
        id_carrera = self.obtener_id_carrera(nombre)
        if id_carrera is None:
            return False, "La carrera no existe."
        consulta = "DELETE FROM carreras WHERE id_carrera = %s;"
        resultado = self.db.ejecutar_consulta(consulta, (id_carrera,))
        if resultado:
            return True, "Carrera eliminada exitosamente."
        else:
            return False, "Error al eliminar la carrera."