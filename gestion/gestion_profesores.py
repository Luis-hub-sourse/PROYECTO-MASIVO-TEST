


from servicios.servicio_profesor import ServicioProfesor



class GestionProfesores:
    def __init__(self):
        self.servicio = ServicioProfesor()
    
    def obtener_estadisticas(self):

        profesores = self.servicio.listar_profesores()
        total_profesores = len(profesores)
        
        return {
            'total_profesores': total_profesores,
            'profesores_registrados': profesores
        }
    
    def buscar_profesores_por_nombre(self, nombre):

        profesores = self.servicio.listar_profesores()
        resultados = []
        
        nombre_busqueda = nombre.lower().strip()
        
        for profesor in profesores:
            if (nombre_busqueda in profesor[1].lower() or 
                nombre_busqueda in profesor[2].lower()):
                resultados.append(profesor)
        
        return resultados
    
    def validar_profesor_completo(self, dni, nombre, apellido, correo, telefono):

        errores = []
        
        if not dni or not dni.strip():
            errores.append("El DNI es obligatorio")
        elif not self.servicio._validar_dni(dni):
            errores.append("El DNI debe tener entre 7 y 8 dígitos")
        
        if not nombre or not nombre.strip():
            errores.append("El nombre es obligatorio")
        
        if not apellido or not apellido.strip():
            errores.append("El apellido es obligatorio")
        
        if not correo or not correo.strip():
            errores.append("El correo es obligatorio")
        elif not self.servicio._validar_correo(correo):
            errores.append("El formato del correo electrónico no es válido")
        
        if not telefono or not telefono.strip():
            errores.append("El teléfono es obligatorio")
        
        return len(errores) == 0, errores