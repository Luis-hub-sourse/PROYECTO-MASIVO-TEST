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
                INSERT INTO alumnos (dni, nombre, ciudad, correo_electronico, apellido, telefono)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (alumno.dni, alumno.nombre, alumno.ciudad, alumno.correo_electronico, alumno.apellido, alumno.telefono))
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
    
    def actualizar_alumno(self, dni_registrado, alumno):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE alumnos 
                SET dni = %s, nombre = %s, ciudad = %s, correo_electronico = %s, apellido = %s, telefono = %s
                WHERE dni = %s
            """, (alumno.dni, alumno.nombre, alumno.ciudad, alumno.correo_electronico, alumno.apellido, alumno.telefono, dni_registrado))
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
    
    def eliminar_alumno(self, dni):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM alumnos WHERE dni = %s", (dni,))
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

