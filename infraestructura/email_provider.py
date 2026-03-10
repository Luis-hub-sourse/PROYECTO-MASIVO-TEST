from email.message import EmailMessage
import smtplib

class EmailProvider:
    def __init__(self, email_usuario, contrasena_app):
        self.email_usuario = email_usuario
        self.contrasena_app = contrasena_app
        
    def enviar_email(self, remitente, destinatario, asunto, mensaje_html):
        try:
            email = EmailMessage()
            email['Subject'] = asunto
            email['From'] = remitente
            email['To'] = destinatario
            email.add_alternative(mensaje_html, subtype='html')
            
            #email.set_content("Notificación de inasistencia. Ver email para detalles.")

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(self.email_usuario, self.contrasena_app)
                smtp.send_message(email)
            return True, "Email enviado exitosamente."
        except Exception as ex:
            return False, f"Error al enviar: {str(ex)}"
    
    def enviar_emails(self, remitente, destinatarios, asunto, mensaje_html):
        try:
            if isinstance(destinatarios, str):
                destinatarios = [destinatarios]
            elif not isinstance(destinatarios, list):
                return False, "destinatarios debe ser string o lista"
            
            email = EmailMessage()
            email['Subject'] = asunto
            email['From'] = remitente
            email['To'] = ', '.join(destinatarios) # Formato para la cabecera
            email.add_alternative(mensaje_html, subtype='html')
            
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(self.email_usuario, self.contrasena_app)
                smtp.send_message(email) 
                
            return True, "Emails enviados exitosamente."
        except Exception as ex:
            return False, f"Error al enviar: {str(ex)}"