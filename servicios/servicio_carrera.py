from repositorio.repositorio_carrera import RepositorioCarrera

class ServicioCarrera:
    def __init__(self):
        self.repositorio = RepositorioCarrera()

    def listar_carreras(self):
        return self.repositorio.listar_carreras()
    
    def agregar_carrera(self, nombre):
        if not nombre:
            return False, "El nombre de la carrera no puede estar vacio."
        exito = self.repositorio.agregar_carrera(nombre)
        if exito:
            return True, "Carrera agregada exitosamente."
        else:
            return False, "Error al agregar la carrera."
        
    def modificar_carrera(self, nombre_original, nuevo_nombre):
        if not nuevo_nombre:
            return False, "El nuevo nombre de la carrera no puede estar vacio."
        elif nombre_original == nuevo_nombre:
            return False, "El nuevo nombre debe ser diferente al original."
        exito = self.repositorio.modificar_carrera(nombre_original, nuevo_nombre)
        if exito:
            return True, "Carrera modificada exitosamente."
        else:
            return False, "Error al modificar la carrera."
    
    def eliminar_carrera(self, nombre):
        exito = self.repositorio.eliminar_carrera(nombre)
        if exito:
            return True, "Carrera eliminada exitosamente."
        else:
            return False, "Error al eliminar la carrera."
    
    def obtener_id_carrera(self, nombre):
        id_carrera = self.repositorio.obtener_id_carrera(nombre)
        if id_carrera is None:
            return False, "La carrera no existe."
        for id in id_carrera:
            id_carrera = id[0]
            return True, id_carrera