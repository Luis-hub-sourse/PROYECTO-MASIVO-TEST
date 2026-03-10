from repositorio.repositorio_inasistencia import RepositorioInasistencia
from servicios.servicio_materia import ServicioMateria
from servicios.servicio_alumno import ServicioAlumno
from entidades.inasistencia import Inasistencia

class ServicioInasistencia:

    def __init__(self):
        self.repositorio = RepositorioInasistencia()
        self.servicio_materia = ServicioMateria()
        self.servicio_alumno = ServicioAlumno()

    def registrar_inasistencia(self, emisor, materia, fecha_falta_qt, fecha_finalizacion_qt, motivo, detalle):
        try:
            id_materia = self.obtener_materia_por_nombre(materia)
            fecha_falta_inicial = fecha_falta_qt.toPyDate()  # Convertir QDate a datetime.date
            if fecha_finalizacion_qt is not None:   fecha_falta_final = fecha_finalizacion_qt.toPyDate()  
            else:   fecha_falta_final = None
            informe = Inasistencia(emisor, id_materia[0], fecha_falta_inicial, fecha_falta_final, motivo, detalle)
            if self.verificar_datos(informe):
                return self.repositorio.registrar_inasistencia(informe)
            return False, "Datos de insasistencia inválidos."
        except Exception as ex:
            return False, f"Ocurrió un error al registrar la inasistencia: {str(ex)}"

    def listar_inasistencias(self):
        inasistencias_raw = self.repositorio.listar_inasistencias()
        inasistencias_final = []
        for registro in inasistencias_raw[1]:
            correo, id_materia, periodo, motivo, detalle, fecha_reg = registro
            
            id_confirmado, nombre_materia = self.obtener_materia_por_id(id_materia)
            
            nuevo_registro = (
                correo,
                nombre_materia,
                periodo,
                motivo,
                detalle,
                fecha_reg
            )
            inasistencias_final.append(nuevo_registro)
        return inasistencias_final
    
    def obtener_materia_por_nombre(self, id_materia):
        materias = self.servicio_materia.buscar_materias()
        for materia in materias:
            if materia[1] == id_materia:
                return materia[0], materia[1]
            
    def obtener_materia_por_id(self, id_materia):
        materias = self.servicio_materia.buscar_materias()
        for materia in materias:
            if materia[0] == id_materia:
                return materia[0], materia[1]
        return None
            
    def obtener_correos_alumnos(self):
        alumnos = self.servicio_alumno.listar_alumnos()
        correos = []
        
        for alumno in alumnos:
            if len(alumno) > 3 and alumno[3]:
                correo = str(alumno[3]).strip()
                if '@' in correo:
                    correos.append(correo)
        
        return correos

    def verificar_datos(self, informe):
        if not informe.emisor or not informe.id_materia or not informe.fecha_falta_inicial or not informe.motivo:
            return False
        return True
    
    def enviar_notificacion(self, emisor, id_materia, fecha_falta_qt, fecha_finalizacion_qt, motivo, detalle):
        try:
            if not emisor or not id_materia or not fecha_falta_qt or not motivo:
                return False, "Datos de insasistencia inválidos para enviar la notificación."

            MESES_ESP = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
            7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
            }

            fecha_falta_inicial = fecha_falta_qt.toPyDate()
            mes_nombre = MESES_ESP[fecha_falta_inicial.month]
            fecha_ini_text = f"{fecha_falta_inicial.day:02d} de {mes_nombre} "
            if fecha_finalizacion_qt is not None:
                fecha_falta_final = fecha_finalizacion_qt.toPyDate()
                mes_nombre = MESES_ESP[fecha_falta_final.month]
                fecha_fin_text = f"""hasta el {fecha_falta_final.day:02d} de {mes_nombre} """
            else:
                fecha_fin_text = " "

            materia_db = self.obtener_materia_por_nombre(id_materia)
            if not materia_db:
                return False, "La materia no existe."

            materia = materia_db[1]
            destinatarios = self.obtener_correos_alumnos()
            asunto = "Nueva inasistencia registrada"

            if detalle is None:
                mensaje_html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px;">
                    <h3 style="color: #d32f2f;">Notificación de inasistencia</h3>
                    <p><strong>Estimados Alumnos:</strong></p>
                    <p>Les escribo para informarles que no podré asistir a la clase de 
                    <strong>{materia}</strong> el <strong>{fecha_ini_text}{fecha_fin_text}</strong>
                    debido a un motivo <strong>{motivo}</strong>.</p>
                </body>
                </html>
                """
            else:
                mensaje_html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px;">
                    <h3 style="color: #d32f2f;">Notificación de inasistencia</h3>
                    <p><strong>Estimados Alumnos:</strong></p>
                    <p>Les escribo para informarles que no podré asistir a la clase de 
                    <strong>{materia}</strong> el <strong>{fecha_ini_text}{fecha_fin_text}</strong>
                    debido a un motivo <strong>{motivo}</strong>.</p>
                    <p><strong>Detalles adicionales:</strong> {detalle}</p>
                </body>
                </html>
                """

            return self.repositorio.enviar_notificacion(emisor, destinatarios, asunto, mensaje_html)
        except Exception as ex:
            return False, f"Ocurrió un error al enviar la notificación: {str(ex)}"

