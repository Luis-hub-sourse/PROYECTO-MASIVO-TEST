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

        # Crear tabla de carrera
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.carreras
            (
                id_carrera uuid NOT NULL DEFAULT gen_random_uuid(),
                nombre character varying(100) COLLATE pg_catalog."default" NOT NULL,
                CONSTRAINT carrera_pkey PRIMARY KEY (id_carrera)
            )
            """
        )

        # Crear tabla de profesores
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.profesores
            (
                dni integer NOT NULL,
                nombre character varying(100) COLLATE pg_catalog."default" NOT NULL,
                ciudad character varying COLLATE pg_catalog."default" NOT NULL,
                correo_electronico character varying(100) COLLATE pg_catalog."default",
                apellido character varying(100) COLLATE pg_catalog."default" NOT NULL,
                telefono character varying(100) COLLATE pg_catalog."default",
                CONSTRAINT profesores_pkey PRIMARY KEY (dni),
                CONSTRAINT uk_correo_profesor UNIQUE (correo_electronico)
            )
            """
        )
        
        # Crear tabla de alumnos
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.alumnos
            (
                dni integer NOT NULL,
                nombre character varying(100) COLLATE pg_catalog."default" NOT NULL,
                ciudad character varying COLLATE pg_catalog."default" NOT NULL,
                correo_electronico character varying(100) COLLATE pg_catalog."default",
                apellido character varying(100) COLLATE pg_catalog."default" NOT NULL,
                telefono character varying(100) COLLATE pg_catalog."default",
                CONSTRAINT alumnos_pkey PRIMARY KEY (dni),
                CONSTRAINT uk_correo_alumno UNIQUE (correo_electronico)
            )
            """
        )
        
        # Crear tabla de materias
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.materias
            (
                id_materia uuid NOT NULL DEFAULT gen_random_uuid(),
                nombre character varying(100) COLLATE pg_catalog."default" NOT NULL,
                "año_cursada" integer NOT NULL,
                carrera_pertenece uuid NOT NULL,
                CONSTRAINT materias_pkey PRIMARY KEY (id_materia),
                CONSTRAINT fk_carrera FOREIGN KEY (carrera_pertenece)
                    REFERENCES public.carreras (id_carrera) MATCH SIMPLE
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                    NOT VALID
            )
            """
        )

        # Crear tabla de usuarios
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.usuarios
            (
                id_usuario uuid NOT NULL DEFAULT gen_random_uuid(),
                correo_electronico character varying(100) COLLATE pg_catalog."default" NOT NULL,
                contrasena character varying COLLATE pg_catalog."default" NOT NULL,
                rol character varying(20) COLLATE pg_catalog."default" NOT NULL,
                CONSTRAINT usuraios_pkey PRIMARY KEY (id_usuario),
                CONSTRAINT uk_correo_usuario UNIQUE (correo_electronico),
                CONSTRAINT check_roles_permitidos CHECK (rol::text = ANY (ARRAY['ADMIN'::character varying, 'ALUMNO'::character varying, 'PROFESOR'::character varying]::text[])) NOT VALID
            )
            """
        )

        # Crear tabla de alumno_materia
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.alumno_materias
            (
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


        # Crear tabla de jornada_materia
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.jornada_materias
            (
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

        # Crear tabla de inasistencias
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public.inasistencias
            (
                id_inasistencia uuid NOT NULL DEFAULT gen_random_uuid(),
                correo_emisor character varying(100) COLLATE pg_catalog."default" NOT NULL,
                id_materia uuid NOT NULL,
                fecha_inasistencia date NOT NULL,
                motivo character varying(50) COLLATE pg_catalog."default",
                detalle text COLLATE pg_catalog."default",
                fecha_registro timestamp without time zone DEFAULT now(),
                CONSTRAINT inasistencias_pkey PRIMARY KEY (id_inasistencia),
                CONSTRAINT inasistencias_id_materia_fkey FOREIGN KEY (id_materia)
                    REFERENCES public.materias (id_materia) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            )
            """
        )

        self.connection.commit()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexion terminada")