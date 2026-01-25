


from servicios.servicio_alumno import ServicioAlumno



class GestionAlumnos:
    def __init__(self):
        self.servicio = ServicioAlumno()
    
    def obtener_estadisticas(self):
        alumnos = self.servicio.listar_alumnos()
        total_alumnos = len(alumnos)
        
        return {
            'total_alumnos': total_alumnos,
            'alumnos_registrados': alumnos
        }
    
    def buscar_alumnos_por_nombre(self, nombre):
        alumnos = self.servicio.listar_alumnos()
        resultados = []
        
        nombre_busqueda = nombre.lower().strip()
        
        for alumno in alumnos:
            if nombre_busqueda in alumno[0].lower():
                resultados.append(alumno)
        
        return resultados
    
    def buscar_alumnos_por_carrera(self, carrera):
        alumnos = self.servicio.listar_alumnos()
        resultados = []
        
        carrera_busqueda = carrera.lower().strip()
        
        for alumno in alumnos:
            if carrera_busqueda in alumno[1].lower():
                resultados.append(alumno)
        
        return resultados
    
    def validar_alumno_completo(self, nombre, carrera, anio):
        errores = []
        
        if not nombre or not nombre.strip():
            errores.append("El nombre es obligatorio")
        
        if not carrera or not carrera.strip():
            errores.append("La carrera es obligatoria")
        
        if not anio or not anio.strip():
            errores.append("El año es obligatorio")
        else:
            try:
                anio_int = int(anio)
                if not (1 <= anio_int <= 10):
                    errores.append("El año debe ser un número válido entre 1 y 10")
            except ValueError:
                errores.append("El año debe ser un número válido entre 1 y 10")
        
        return len(errores) == 0, errores

