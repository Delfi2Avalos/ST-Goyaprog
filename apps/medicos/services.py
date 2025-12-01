from django.db import connection
import bcrypt
import requests
from firebase_admin import db as firebase_db

URL_ESTADO_TURNO = "https://us-central1-salud-total-a0d92.cloudfunctions.net/auditoria-auditarTurno"

class MedicoService:

    @staticmethod
    def ver_turnos(medico_id):
        sql = """
            SELECT 
                t.id, t.fecha, t.hora, t.estado, t.detalles,
                u.nombre AS paciente_nombre, u.apellido AS paciente_apellido, u.obra_social
            FROM turnos t
            JOIN usuarios u ON t.paciente_id = u.id
            WHERE t.medico_id = %s
            ORDER BY t.fecha, t.hora
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [medico_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def actualizar_estado_turno(turno_id, estado):
        estados_permitidos = [
            'confirmado', 'cancelado', 'atendido', 'rechazado_medico'
        ]
        if estado not in estados_permitidos:
            return None, "Estado inválido"

        sql_datos = """
            SELECT t.id, t.fecha, t.hora,
                   u.email AS paciente_email,
                   u.nombre AS paciente_nombre
            FROM turnos t
            JOIN usuarios u ON t.paciente_id = u.id
            WHERE t.id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_datos, [turno_id])
            datos = cursor.fetchone()

        if not datos:
            return None, "Turno no encontrado"

        turno = {
            "id": datos[0],
            "fecha": datos[1],
            "hora": datos[2],
            "paciente_email": datos[3],
            "paciente_nombre": datos[4],
        }

        sql_update = """
            UPDATE turnos
            SET estado = %s, fecha_actualizacion_estado = NOW()
            WHERE id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_update, [estado, turno_id])

        try:
            requests.post(URL_ESTADO_TURNO, {
                "turnoId": turno_id,
                "nuevoEstado": estado,
                "paciente_email": turno["paciente_email"],
                "paciente_nombre": turno["paciente_nombre"],
                "fecha": turno["fecha"],
                "hora": turno["hora"]
            })
        except Exception:
            pass

        return True, None

    @staticmethod
    def obtener_horarios(medico_id):
        sql = """
            SELECT dia_semana, hora_inicio, hora_fin
            FROM horarios_medicos
            WHERE medico_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [medico_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def actualizar_horarios(medico_id, horarios):
        eliminar_sql = "DELETE FROM horarios_medicos WHERE medico_id = %s"

        with connection.cursor() as cursor:
            cursor.execute(eliminar_sql, [medico_id])

            if not horarios:
                return True

            insert_sql = """
                INSERT INTO horarios_medicos (medico_id, dia_semana, hora_inicio, hora_fin)
                VALUES (%s, %s, %s, %s)
            """
            for h in horarios:
                cursor.execute(insert_sql, [
                    medico_id, h["dia_semana"], h["hora_inicio"], h["hora_fin"]
                ])

        return True

    @staticmethod
    def horas_ocupadas(medico_id, fecha):
        sql = """
            SELECT TIME_FORMAT(hora, '%H:%i') AS hora
            FROM turnos
            WHERE medico_id = %s AND fecha = %s
            AND estado IN ('en espera', 'confirmado')
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [medico_id, fecha])
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def cambiar_password(medico_id, nueva_contra):
        hashed = bcrypt.hashpw(nueva_contra.encode(), bcrypt.gensalt())

        sql = """
            UPDATE usuarios SET contrasena = %s
            WHERE id = %s AND tipo = 'medico'
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [hashed, medico_id])

        return True

    @staticmethod
    def buscar_paciente(nombre, apellido):
        sql = """
            SELECT id, nombre, apellido, email, obra_social
            FROM usuarios
            WHERE tipo = 'paciente' AND nombre = %s AND apellido = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [nombre, apellido])
            row = cursor.fetchone()

        if not row:
            return None
        return {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "email": row[3],
            "obra_social": row[4]
        }

    @staticmethod
    def crear_formulario(medico_id, nombre_completo, contenido):
        sql = """
            INSERT INTO formularios_medicos (medico_id, nombre_completo, contenido)
            VALUES (%s, %s, %s)
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [medico_id, nombre_completo, contenido])
            formulario_id = cursor.lastrowid

        # Firebase
        try:
            ruta = f"historiales/{nombre_completo.replace(' ', '_')}"
            ref = firebase_db.reference(ruta).push()
            ref.set({
                "formulario_id": formulario_id,
                "medico_id": medico_id,
                "nombre_completo": nombre_completo,
                "contenido": contenido,
                "fecha": firebase_db.ServerValue.TIMESTAMP
            })
        except Exception:
            pass

        return True

    @staticmethod
    def editar_formulario(formulario_id, contenido, nombre_completo):
        sql = """
            UPDATE formularios_medicos
            SET contenido = %s
            WHERE id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [contenido, formulario_id])

        try:
            ruta = f"historiales/{nombre_completo.replace(' ', '_')}"
            ref = firebase_db.reference(ruta)
            ref.update({
                "ultima_actualizacion": firebase_db.ServerValue.TIMESTAMP,
                "contenido_actualizado": contenido,
            })
        except Exception:
            pass

        return True

    @staticmethod
    def listar_formularios(medico_id):
        sql = """
            SELECT * FROM formularios_medicos
            WHERE medico_id = %s
            ORDER BY fecha DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [medico_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def buscar_formularios_por_nombre(nombre):
        sql = """
            SELECT *
            FROM formularios_medicos
            WHERE nombre_completo LIKE %s
            ORDER BY fecha DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [f"%{nombre}%"])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
