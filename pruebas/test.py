if detalle is None:
                mensaje = f"""
                Asunto: Notificación de inasistencia
                
                Estimados Alumnos:
                
                Les escribo para informarles que no podré asistir a la clase de {materia} el {fecha_falta_inicial:%d de %B}{fecha_fin_text}debido a tema {motivo}."""
            else:
                mensaje = f"""
                Asunto: Notificación de inasistencia
                
                Estimados Alumnos:
                
                Les escribo para informarles que no podré asistir a la clase de {materia} el {fecha_falta_inicial:%d de %B}{fecha_fin_text}debido a tema {motivo}.
                
                Detalles adicionales: {detalle}"""