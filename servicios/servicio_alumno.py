from repositorio.repositorio_alumno import RepositorioAlumno
from entidades.alumnos import Alumno

class ServicioAlumno:
    def __init__(self):
        self.repositorio = RepositorioAlumno()
    
    def listar_alumnos(self):
        return self.repositorio.listar_alumnos()
    
    def buscar_alumno(self, nombre: str):
        return self.repositorio.buscar_alumno(nombre)
    
    def agregar_alumno(self, nombre: str, carrera: str, anio: str):
        # Validar datos
        if not self._validar_datos(nombre, carrera, anio):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_anio(anio):
            return False, "El año debe ser un número válido"
        
        alumno = Alumno(nombre, carrera, anio)
        exito, mensaje = self.repositorio.agregar_alumno(alumno)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    
    def actualizar_alumno(self, nombre_original: str, nombre: str, carrera: str, anio: str):
        # Validar datos
        if not self._validar_datos(nombre, carrera, anio):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_anio(anio):
            return False, "El año debe ser un número válido"
        
        alumno = Alumno(nombre, carrera, anio)
        exito, mensaje = self.repositorio.actualizar_alumno(nombre_original, alumno)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    
    def eliminar_alumno(self, nombre: str):
        if not nombre or not nombre.strip():
            return False, "El nombre es obligatorio"
        
        resultado = self.repositorio.eliminar_alumno(nombre)
        
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

