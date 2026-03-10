class Inasistencia:
    def __init__(self, correo_emisor, id_materia, fecha_inasistencia_inicial, fecha_inasistencia_final, motivo, detalle):
        self.emisor = correo_emisor
        self.id_materia = id_materia
        self.fecha_falta_inicial = fecha_inasistencia_inicial
        self.fecha_falta_final = fecha_inasistencia_final
        self.motivo = motivo
        self.detalle = detalle