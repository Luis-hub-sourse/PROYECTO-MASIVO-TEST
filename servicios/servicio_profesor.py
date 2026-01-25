from repositorio.repositorio_profesor import RepositorioProfesor
from entidades.profesores import Profesor

class ServicioProfesor:
    def __init__(self):
        self.repositorio = RepositorioProfesor()
    

    def listar_profesores(self):

        return self.repositorio.listar_profesores()
    

    def buscar_profesor(self, dni: str):

        return self.repositorio.buscar_profesor(dni)
    

    def agregar_profesor(self, dni: str, nombre: str, apellido: str, correo: str, telefono: str):

        # Validar datos
        if not self._validar_datos(dni, nombre, apellido, correo, telefono):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_dni(dni):
            return False, "El DNI debe tener entre 7 y 8 dígitos"
        
        if not self._validar_correo(correo):
            return False, "El formato del correo electrónico no es válido"
        
        profesor = Profesor(dni, nombre, apellido, correo, telefono)
        exito, mensaje = self.repositorio.agregar_profesor(profesor)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    

    def actualizar_profesor(self, dni: str, nombre: str, apellido: str, correo: str, telefono: str):

        # Validar datos
        if not self._validar_datos(dni, nombre, apellido, correo, telefono):
            return False, "Todos los campos son obligatorios"
        
        if not self._validar_correo(correo):
            return False, "El formato del correo electrónico no es válido"
        
        profesor = Profesor(dni, nombre, apellido, correo, telefono)
        exito, mensaje = self.repositorio.actualizar_profesor(profesor)
        
        if exito:
            return True, mensaje
        else:
            return False, mensaje
    

    def eliminar_profesor(self, dni: str):

        if not dni or not dni.strip():
            return False, "El DNI es obligatorio"
        
        resultado = self.repositorio.eliminar_profesor(dni)
        
        if resultado[0]:
            return True, resultado[1]
        else:
            return False, resultado[1]
    

    def _validar_datos(self, dni: str, nombre: str, apellido: str, correo: str, telefono: str) -> bool:

        return all([dni and dni.strip(), nombre and nombre.strip(), 
                   apellido and apellido.strip(), correo and correo.strip(), 
                   telefono and telefono.strip()])
    

    def _validar_dni(self, dni: str) -> bool:

        dni_limpio = dni.strip().replace(".", "").replace("-", "")
        return dni_limpio.isdigit() and 7 <= len(dni_limpio) <= 8
    

    def _validar_correo(self, correo: str) -> bool:

        import re
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, correo) is not None