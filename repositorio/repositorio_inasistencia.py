from db.connexion_posgreSQL import ConexionDB
from infraestructura.email_provider import EmailProvider

class RepositorioInasistencia:

    def __init__(self):
        self.conexion = ConexionDB()

    def registrar_inasistencia(self, informe):
        consulta = """ \
            INSERT INTO inasistencias (correo_emisor, id_materia, fecha_de_inicio, fecha_de_finalizacion, motivo, detalle) \
            VALUES (%s, %s, %s, %s, %s, %s);
            """
        datos = (informe.emisor, informe.id_materia, informe.fecha_falta_inicial, informe.fecha_falta_final, informe.motivo, informe.detalle)
        exito = self.conexion.ejecutar_consulta(consulta, datos)
        if exito:
            return True, "Inasistencia registrada exitosamente."
        return False, "Error al registrar la inasistencia."
        

    def listar_inasistencias(self):
        consulta = "SELECT \
            correo_emisor, \
            id_materia, \
            CASE \
                WHEN fecha_de_finalizacion IS NULL \
                THEN TO_CHAR(fecha_de_inicio, 'YYYY/MM/DD') \
                ELSE TO_CHAR(fecha_de_inicio, 'YYYY/MM/DD') || '-' || \
                    TO_CHAR(fecha_de_finalizacion, 'YYYY/MM/DD') \
            END AS periodo_falta, \
            motivo, \
            detalle, \
            TO_CHAR(fecha_registro, 'YYYY/MM/DD HH24:MI:SS') AS fecha_registro \
            FROM inasistencias"
        resultados = self.conexion.obtencion(consulta, ())
        if resultados is not None:
            return True, resultados
        return False, "Error al obtener los registros de inasistencias."
    
    def enviar_notificacion(self, remitente, destinatario, asunto, mensaje):
        email_provider = EmailProvider('funciondeprueba@gmail.com', 'rnoq umtu ejet kvoe')
        exito, resultado = email_provider.enviar_emails(remitente, destinatario, asunto, mensaje)
        if exito:
            return True, resultado
        return False, resultado