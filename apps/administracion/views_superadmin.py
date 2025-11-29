from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from apps.administracion.permissions import IsSuperAdmin
from django.conf import settings
import requests
import bcrypt

URL_CORREO_ALTA = "https://us-central1-salud-total-a0d92.cloudfunctions.net/correos-correoAltaUsuario"


# 1. Listar médicos por especialidad
@api_view(["GET"])
@permission_classes([IsSuperAdmin])
def listar_medicos_por_especialidad(request, especialidad_id):

    sql = """
        SELECT u.id, u.nombre, u.apellido, u.email
        FROM usuarios u
        JOIN medico_especialidades me ON u.id = me.medico_id
        WHERE me.especialidad_id = %s AND u.tipo = 'medico'
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [especialidad_id])
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    return Response(resultados, status=200)


# 2. Contar pacientes atendidos
@api_view(["GET"])
@permission_classes([IsSuperAdmin])
def contar_pacientes_atendidos(request, medico_id):

    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")

    sql = """
        SELECT COUNT(*) AS cantidad
        FROM turnos
        WHERE medico_id = %s AND estado = 'atendido'
    """
    params = [medico_id]

    if desde and hasta:
        sql += " AND fecha BETWEEN %s AND %s"
        params.extend([desde, hasta])

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        cantidad = cursor.fetchone()[0]

    return Response({"cantidad": cantidad})


# 3. Registrar nuevo médico
@api_view(["POST"])
@permission_classes([IsSuperAdmin])
def registrar_medico(request):

    data = request.data
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    contrasena = data.get("contrasena")
    especialidades = data.get("especialidades", [])
    horarios = data.get("horarios", [])

    if not nombre or not apellido or not email or not contrasena:
        return Response(
            {"mensaje": "Faltan campos obligatorios."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Hashear contraseña 
    hash_pw = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode()

    # Insertar médico
    sql_usuario = """
        INSERT INTO usuarios (nombre, apellido, email, contrasena, tipo)
        VALUES (%s, %s, %s, %s, 'medico')
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_usuario, [nombre, apellido, email, hash_pw])
        medico_id = cursor.lastrowid

    # Asignar especialidades
    if isinstance(especialidades, list) and len(especialidades) > 0:
        sql_es = """
            INSERT INTO medico_especialidades (medico_id, especialidad_id)
            VALUES (%s, %s)
        """
        with connection.cursor() as cursor:
            for esp in especialidades:
                cursor.execute(sql_es, [medico_id, esp])

    # Registrar horarios
    if isinstance(horarios, list) and len(horarios) > 0:
        sql_h = """
            INSERT INTO horarios_medicos (medico_id, dia_semana, hora_inicio, hora_fin)
            VALUES (%s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            for h in horarios:
                cursor.execute(sql_h, [medico_id, h["dia_semana"], h["hora_inicio"], h["hora_fin"]])

    # Enviar correo por Cloud Function
    try:
        requests.post(URL_CORREO_ALTA, json={
            "nombre": nombre,
            "email": email,
            "tipo": "medico"
        })
    except Exception as e:
        print("Error enviando correo:", e)

    return Response({"mensaje": "Médico registrado correctamente."}, status=201)


# 4. Crear secretario (admin)
@api_view(["POST"])
@permission_classes([IsSuperAdmin])
def crear_secretario(request):
    data = request.data

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    contrasena = data.get("contrasena")

    if not nombre or not apellido or not email or not contrasena:
        return Response(
            {"mensaje": "Faltan campos obligatorios."},
            status=400
        )

    hash_pw = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode()

    sql = """
        INSERT INTO usuarios (nombre, apellido, email, contrasena, tipo)
        VALUES (%s, %s, %s, %s, 'admin')
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [nombre, apellido, email, hash_pw])

    return Response({"mensaje": "Secretario creado correctamente."}, status=201)


# 5. Obtener formularios
@api_view(["GET"])
@permission_classes([IsSuperAdmin])
def obtener_formularios(request):

    nombre_completo = request.GET.get("nombre_completo")
    medico_email = request.GET.get("medico_email")

    sql = """
        SELECT 
          f.id, f.nombre_completo, f.contenido, f.fecha,
          u.nombre AS medico_nombre, u.apellido AS medico_apellido, u.email AS medico_email
        FROM formularios_medicos f
        LEFT JOIN usuarios u ON f.medico_id = u.id
        WHERE 1 = 1
    """
    params = []

    if nombre_completo:
        sql += " AND f.nombre_completo LIKE %s"
        params.append(f"%{nombre_completo}%")

    if medico_email:
        sql += " AND u.email LIKE %s"
        params.append(f"%{medico_email}%")

    sql += " ORDER BY f.fecha DESC"

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    return Response(resultados)
