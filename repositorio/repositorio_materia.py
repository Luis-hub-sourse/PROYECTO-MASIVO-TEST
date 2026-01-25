from db.connexion_posgreSQL import ConexionDB
import psycopg2

class RepositorioMateria:
    def __init__(self):
        self.db = ConexionDB()

    def listar_materias(self):
        conexion = self.db.connect_to_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM materias ORDER BY nombre")
        materias = cursor.fetchall()
        cursor.close()
        conexion.close()
        return materias
    
    def buscar_materia(self, nombre):
        conexion = self.db.connect_to_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM materias WHERE nombre = %s", (nombre,))
        materia = cursor.fetchone()
        cursor.close()
        conexion.close()
        return materia
    
    def agregar_materia(self, materia):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO materias (nombre, carrera, anio)
                VALUES (%s, %s, %s)
            """, (materia.nombre, materia.carrera, materia.anio))
            conexion.commit()
            cursor.close()
            conexion.close()
            return True, "Materia agregada exitosamente"
        except psycopg2.IntegrityError as e:
            conexion.rollback()
            cursor.close()
            conexion.close()
            return False, "Ya existe una materia con este nombre"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error de base de datos: {str(e)}"
    
    def actualizar_materia(self, nombre_original, materia):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE materias 
                SET nombre = %s, carrera = %s, anio = %s
                WHERE nombre = %s
            """, (materia.nombre, materia.carrera, materia.anio, nombre_original))
            conexion.commit()
            actualizadas = cursor.rowcount
            cursor.close()
            conexion.close()
            if actualizadas > 0:
                return True, "Materia actualizada exitosamente"
            else:
                return False, "No se encontró la materia con ese nombre"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error al actualizar materia: {str(e)}"
    
    def eliminar_materia(self, nombre):
        try:
            conexion = self.db.connect_to_db()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM materias WHERE nombre = %s", (nombre,))
            conexion.commit()
            eliminadas = cursor.rowcount
            cursor.close()
            conexion.close()
            if eliminadas > 0:
                return True, "Materia eliminada exitosamente"
            else:
                return False, "No se encontró la materia con ese nombre"
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                try:
                    cursor.close()
                except Exception:
                    pass
                conexion.close()
            return False, f"Error al eliminar materia: {str(e)}"

