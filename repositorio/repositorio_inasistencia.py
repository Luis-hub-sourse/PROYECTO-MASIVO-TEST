from db.connexion_posgreSQL import ConexionDB

class RepositorioInasistencia:

    def __init__(self):
        self.conexion = ConexionDB()

    def registrar_inasistencia(self, informe):
        consulta = """ \
            INSERT INTO inasistencias (correo_emisor, id_materia, fecha_inasistencia, motivo, detalle) \
            VALUES (%s, %s, %s, %s, %s)
            """, (informe.emisor, informe.id_materia, informe.fecha_falta, informe.motivo, informe.detalle)
        exito = self.conexion.ejecutar_consulta(consulta)
        if exito:
            return True, "Inasistencia registrada con éxito."
        return False, "Error al registrar la inasistencia."
        

    def listar_inasistencias(self):
        consulta = "SELECT correo_emisor, id_materia, fecha_inasistencia, motivo, detalle FROM inasistencias"
        resultados = self.conexion.obtencion(consulta)
        if resultados is not None:
            return True, resultados
        return False, "Error al obtener los registros de inasistencias."
