import psycopg2

class ConexionDB:
    def __init__(self):
        self.connection = self.connect_to_db()
        self.inicializar_base_datos()

    def connect_to_db(self):
        connection = psycopg2.connect(
            user="postgres",
            password="123456",
            host="localhost",
                database="postgres"
            )
        return connection
    
    def ejecutar_consulta(self, consulta, datos):
        try:
            cursor = self.connection.cursor()
            cursor.execute(consulta, datos)
            self.connection.commit()
            return True
        except Exception as ex:
            print(ex)
            print("Error en la consulta")
            return False
        
    def obtencion(self, consulta, dato):
        try:
            cursor = self.connection.cursor()
            cursor.execute(consulta, dato)
            muestra = cursor.fetchall()
            self.connection.commit()
            return muestra
        except Exception as ex:
            print("Obtecion: ", ex)
            return None
        
    def inicializar_base_datos(self):

        cursor = self.connection.cursor()

        # Crear tabla de profesores
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.profesores(
                dni integer NOT NULL,
                nombre character varying(100) NOT NULL,
                ciudad character varying NOT NULL,
                correo_electronico character varying(100) NOT NULL,
                apellido character varying(100) NOT NULL,
                telefono character varying(100),

                CONSTRAINT profesores_pkey PRIMARY KEY (dni),
                CONSTRAINT uk_correo_profesor UNIQUE (correo_electronico)
            )
            """
        )
        
        # Crear tabla de alumnos
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.alumnos(
                dni integer NOT NULL,
                nombre character varying(100) NOT NULL,
                ciudad character varying NOT NULL,
                correo_electronico character varying(100) NOT NULL,
                apellido character varying(100) NOT NULL,
                telefono character varying(100),

                CONSTRAINT alumnos_pkey PRIMARY KEY (dni),
                CONSTRAINT uk_correo_alumno UNIQUE (correo_electronico)
            )
            """
        )
        
        # Crear tabla de materias
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.materias(
                id_materia uuid NOT NULL DEFAULT gen_random_uuid(),
                nombre character varying(100) NOT NULL,
                "año_cursada" integer NOT NULL,
                carrera_pertenece uuid NOT NULL,

                CONSTRAINT materias_pkey PRIMARY KEY (id_materia),
                CONSTRAINT fk_carrera FOREIGN KEY (carrera_pertenece)
                    REFERENCES public.carrera (id_carrera) MATCH SIMPLE
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
            """
        )

        # Crear tabla de usuarios
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.usuarios(
                id_usuario uuid NOT NULL DEFAULT gen_random_uuid(),
                correo_electronico character varying(100) NOT NULL,
                contrasena character varying NOT NULL,
                rol character varying(20) NOT NULL,

                CONSTRAINT usuraios_pkey PRIMARY KEY (id_usuario),
                CONSTRAINT uk_correo_usuario UNIQUE (correo_electronico),
                CONSTRAINT check_roles_permitidos CHECK (rol::text = ANY (ARRAY['ADMIN'::character varying, 'ALUMNO'::character varying, 'PROFESOR'::character varying]::text[])) NOT VALID
            )
            """
        )

        # Crear tabla de alumno_materia
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.alumno_materia(
                alumno integer NOT NULL,
                materia uuid NOT NULL,
                "año_cursada" integer NOT NULL,
                nota_final integer,
                aprobada boolean,
                fecha_aprobacion date,

                CONSTRAINT alumno_materia_pkey PRIMARY KEY (alumno, materia, "año_cursada"),
                CONSTRAINT fk_alumno FOREIGN KEY (alumno)
                    REFERENCES public.alumnos (dni) MATCH SIMPLE
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,

                CONSTRAINT fk_materia FOREIGN KEY (materia)
                    REFERENCES public.materias (id_materia) MATCH SIMPLE
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
            """
        )

        # Crear tabla de carrera
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.carrera(
                id_carrera uuid NOT NULL DEFAULT gen_random_uuid(),
                nombre character varying(100) NOT NULL,

                CONSTRAINT carrera_pkey PRIMARY KEY (id_carrera)
            )
            """
        )

        # Crear tabla de jornada_materia
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.jornada_materia(
                materia uuid NOT NULL,
                dia_semana integer NOT NULL,
                hora_inicial time without time zone NOT NULL,
                hora_final time without time zone NOT NULL,

                CONSTRAINT jornada_materia_pkey PRIMARY KEY (materia, dia_semana),
                CONSTRAINT fk_materia FOREIGN KEY (materia)
                    REFERENCES public.materias (id_materia) MATCH SIMPLE
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                    
                CONSTRAINT check_horario CHECK (hora_final > hora_inicial) NOT VALID
            )
            """
        )

        self.connection.commit()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexion terminada")