from db.connexion_posgreSQL import ConexionDB 
import psycopg2

class RepositorioAlumno:
    def __init__(self):
        self.db = ConexionDB()

    def listar_alumnos(self):
        conexion = self.db.connect_to_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos ORDER BY nombre")
        alumnos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return alumnos
    
    def buscar_alumno(self, nombre):
        conexion = self.db.connect_to_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos WHERE nombre = %s", (nombre,))
        alumno = cursor.fetchone()
        cursor.close()
        conexion.close()
        return alumno
    
    def agregar_alumno(self, alumno):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO alumnos (nombre, carrera, anio)
                VALUES (%s, %s, %s)
            """, (alumno.nombre, alumno.carrera, alumno.anio))
            conexion.commit()
            cursor.close()
            conexion.close()
            return True, "Alumno agregado exitosamente"
        except psycopg2.IntegrityError as e:
            conexion.rollback()
            cursor.close()
            conexion.close()
            return False, "Ya existe un alumno con este nombre"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error de base de datos: {str(e)}"
    
    def actualizar_alumno(self, nombre_original, alumno):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE alumnos 
                SET nombre = %s, carrera = %s, anio = %s
                WHERE nombre = %s
            """, (alumno.nombre, alumno.carrera, alumno.anio, nombre_original))
            conexion.commit()
            actualizadas = cursor.rowcount
            cursor.close()
            conexion.close()
            if actualizadas > 0:
                return True, "Alumno actualizado exitosamente"
            else:
                return False, "No se encontró el alumno con ese nombre"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error al actualizar alumno: {str(e)}"
    
    def eliminar_alumno(self, nombre):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM alumnos WHERE nombre = %s", (nombre,))
            conexion.commit()
            eliminadas = cursor.rowcount
            cursor.close()
            conexion.close()
            if eliminadas > 0:
                return True, "Alumno eliminado exitosamente"
            else:
                return False, "No se encontró el alumno con ese nombre"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error al eliminar alumno: {str(e)}"

