from db.connexion_posgreSQL import ConexionDB
import psycopg2


class RepositorioProfesor:
    def __init__(self):
        self.db = ConexionDB()

    def listar_profesores(self):

        conexion = self.db.connect_to_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM profesores ORDER BY apellido, nombre")
        profesores = cursor.fetchall()
        cursor.close()
        conexion.close()
        return profesores
    

    def buscar_profesor(self, dni):

        conexion = self.db.connect_to_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM profesores WHERE dni = %s", (dni,))
        profesor = cursor.fetchone()
        cursor.close()
        conexion.close()
        return profesor
    

    def agregar_profesor(self, profesor):

        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO profesores (dni, nombre, apellido, correo, telefono)
                VALUES (%s, %s, %s, %s, %s)
            """, (profesor.dni, profesor.nombre, profesor.apellido, profesor.correo, profesor.telefono))
            conexion.commit()
            cursor.close()
            conexion.close()
            return True, "Profesor agregado exitosamente"

        except psycopg2.IntegrityError as e:
            conexion.rollback()
            cursor.close()
            conexion.close()
            return False, "Ya existe un profesor con este DNI"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error de base de datos: {str(e)}"
    

    def actualizar_profesor(self, profesor):

        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE profesores 
                SET nombre = %s, apellido = %s, correo = %s, telefono = %s
                WHERE dni = %s
            """, (profesor.nombre, profesor.apellido, profesor.correo, profesor.telefono, profesor.dni))
            conexion.commit()
            actualizadas = cursor.rowcount
            cursor.close()
            conexion.close()
            if actualizadas > 0:
                return True, "Profesor actualizado exitosamente"
            else:
                return False, "No se encontró el profesor con ese DNI"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error al actualizar profesor: {str(e)}"
    
    def eliminar_profesor(self, dni):

        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM profesores WHERE dni = %s", (dni,))
            conexion.commit()
            eliminadas = cursor.rowcount
            cursor.close()
            conexion.close()
            if eliminadas > 0:
                return True, "Profesor eliminado exitosamente"
            else:
                return False, "No se encontró el profesor con ese DNI"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error al eliminar profesor: {str(e)}"