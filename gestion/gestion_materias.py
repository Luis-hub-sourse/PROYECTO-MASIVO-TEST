


from servicios.servicio_materia import ServicioMateria



class GestionMaterias:
    def __init__(self):
        self.servicio = ServicioMateria()
    
    def obtener_estadisticas(self):
        materias = self.servicio.listar_materias()
        total_materias = len(materias)
        
        return {
            'total_materias': total_materias,
            'materias_registradas': materias
        }
    
    def buscar_materias_por_nombre(self, nombre):
        materias = self.servicio.listar_materias()
        resultados = []
        
        nombre_busqueda = nombre.lower().strip()
        
        for materia in materias:
            if nombre_busqueda in materia[0].lower():
                resultados.append(materia)
        
        return resultados
    
    def buscar_materias_por_carrera(self, carrera):
        materias = self.servicio.listar_materias()
        resultados = []
        
        carrera_busqueda = carrera.lower().strip()
        
        for materia in materias:
            if carrera_busqueda in materia[1].lower():
                resultados.append(materia)
        
        return resultados
    
    def validar_materia_completa(self, nombre, carrera, anio):
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

