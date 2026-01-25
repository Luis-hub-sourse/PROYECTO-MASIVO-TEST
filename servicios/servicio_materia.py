from repositorio.repositorio_materia import RepositorioMateria
from entidades.materias import Materia


class ServicioMateria:
    def __init__(self):
        self.repositorio = RepositorioMateria()
    
    def listar_materias(self):
        return self.repositorio.listar_materias()
    
    def buscar_materia(self, nombre: str):
        return self.repositorio.buscar_materia(nombre)
    
    def agregar_materia(self, nombre: str, carrera: str, anio: str):
        # Validar datos
        if not self._validar_datos(nombre, carrera, anio):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_anio(anio):
            return False, "El año debe ser un número válido entre 1 y 10"
        
        materia = Materia(nombre, carrera, anio)
        exito, mensaje = self.repositorio.agregar_materia(materia)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    
    def modificar_materia(self, nombre_original: str, nombre: str, carrera: str, anio: str):
        # Validar datos
        if not self._validar_datos(nombre, carrera, anio):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_anio(anio):
            return False, "El año debe ser un número válido entre 1 y 10"
        
        materia = Materia(nombre, carrera, anio)
        exito, mensaje = self.repositorio.actualizar_materia(nombre_original, materia)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    
    def eliminar_materia(self, nombre: str):
        if not nombre or not nombre.strip():
            return False, "El nombre es obligatorio"
        
        resultado = self.repositorio.eliminar_materia(nombre)
        
        if resultado[0]:
            return True, resultado[1]
        else:
            return False, resultado[1]
    
    def _validar_datos(self, nombre: str, carrera: str, anio: str) -> bool:
        return all([nombre and nombre.strip(), carrera and carrera.strip(), anio and anio.strip()])
    
    def _validar_anio(self, anio: str) -> bool:
        try:
            anio_int = int(anio)
            return 1 <= anio_int <= 10  # Validar que el año sea razonable (1-10)
        except ValueError:
            return False

