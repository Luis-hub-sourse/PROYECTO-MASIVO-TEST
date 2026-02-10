from repositorio.repositorio_inasistencia import RepositorioInasistencia
from entidades.inasistencia import Inasistencia

class ServicioInasistencia:

    def __init__(self):
        self.repositorio = RepositorioInasistencia()

    def registrar_inasistencia(self, emisor, id_materia, fecha_falta, motivo, detalle):
        informe = Inasistencia(emisor, id_materia, fecha_falta, motivo, detalle)
        if self.verificar_datos(informe):
            return self.repositorio.registrar_inasistencia(informe)
        return False, "Datos de insasistencia inválidos."

    def listar_inasistencias(self):
        pass

    def verificar_datos(self, informe):
        if not informe.emisor or not informe.id_materia or not informe.fecha_falta or not informe.motivo:
            return False
        return True