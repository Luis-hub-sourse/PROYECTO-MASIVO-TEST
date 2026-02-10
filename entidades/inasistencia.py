class Inasistencia:
    def __init__(self, correo_emisor, id_materia, fecha_inasistencia, motivo, detalle):
        self.emisor = correo_emisor
        self.id_materia = id_materia
        self.fecha_falta = fecha_inasistencia
        self.motivo = motivo
        self.detalle = detalle