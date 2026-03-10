from repositorio.repositorio_alumno import RepositorioAlumno
from entidades.alumnos import Alumno

class ServicioAlumno:
    def __init__(self):
        self.repositorio = RepositorioAlumno()
    
    def listar_alumnos(self):
        return self.repositorio.listar_alumnos()
    
    def buscar_alumno(self, nombre: str):
        return self.repositorio.buscar_alumno(nombre)
    
    def agregar_alumno(self, dni, nombre, apellido, correo, telefono, ciudad):
        # Validar datos
        if not self._validar_datos(dni, nombre, apellido, correo, telefono, ciudad):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_anio(dni):
            return False, "El dni debe ser un número válido"
        
        alumno = Alumno(dni, nombre, apellido, correo, telefono, ciudad)
        exito, mensaje = self.repositorio.agregar_alumno(alumno)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    
    def actualizar_alumno(self, dni_registrado, dni, nombre, apellido, correo, telefono, ciudad):
        # Validar datos
        if not self._validar_datos(dni, nombre, apellido, correo, telefono, ciudad):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_anio(dni):
            return False, "El dni debe ser un número válido"
        
        alumno = Alumno(dni, nombre, apellido, correo, telefono, ciudad)
        exito, mensaje = self.repositorio.actualizar_alumno(dni_registrado, alumno)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    
    def eliminar_alumno(self, dni: str):
        if not dni or not dni.strip():
            return False, "El dni es obligatorio"
        
        resultado = self.repositorio.eliminar_alumno(dni)
        
        if resultado[0]:
            return True, resultado[1]
        else:
            return False, resultado[1]
    
    def _validar_datos(self, dni, nombre, apellido, correo, telefono, ciudad) -> bool:
        return all([dni and dni.strip(), nombre and nombre.strip(), apellido and apellido.strip(), correo and correo.strip(), telefono and telefono.strip(), ciudad and ciudad.strip()])
    
    def _validar_anio(self, dni) -> bool:
        try:
            dni_int = int(dni)
            return dni_int <= 100000000  # Validar que el dni sea razonable (1-10)
        except ValueError:
            return False

