from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db import connection

from .permissions import IsAdmin, IsSuperAdmin


# 1. Listar médicos por especialidad
@api_view(["GET"])
@permission_classes([IsAdmin])
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

    return Response(resultados, status=status.HTTP_200_OK)


# 2. Contar pacientes atendidos (rango de fechas opcional)
@api_view(["GET"])
@permission_classes([IsAdmin])
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


# 3. Obtener formularios (filtros opcionales)
@api_view(["GET"])
@permission_classes([IsAdmin])
def obtener_formularios(request):
    nombre_completo = request.GET.get("nombre_completo")
    medico_email = request.GET.get("medico_email")

    sql = """
        SELECT 
            f.id, f.nombre_completo, f.contenido, f.fecha,
            u.nombre AS medico_nombre, u.apellido AS medico_apellido, u.email AS medico_email
        FROM formularios_medicos f
        LEFT JOIN usuarios u ON f.medico_id = u.id
        WHERE 1=1
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
        columnas = [c[0] for c in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    return Response(resultados)


# 4. Listar todos los turnos
@api_view(["GET"])
@permission_classes([IsAdmin])
def listar_turnos(request):
    sql = """
        SELECT 
            t.id, t.fecha, t.hora, t.estado,
            p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
            m.nombre AS medico_nombre, m.apellido AS medico_apellido,
            e.nombre AS especialidad
        FROM turnos t
        JOIN usuarios p ON t.paciente_id = p.id
        LEFT JOIN usuarios m ON t.medico_id = m.id
        JOIN especialidades e ON t.especialidad_id = e.id
        ORDER BY t.fecha DESC, t.hora ASC
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    return Response(resultados)


# 5. Actualizar estado del turno
@api_view(["PUT"])
@permission_classes([IsAdmin])
def actualizar_estado_turno(request):
    turno_id = request.data.get("turno_id")
    nuevo_estado = request.data.get("nuevo_estado")

    if not turno_id or not nuevo_estado:
        return Response({"mensaje": "Faltan datos."},
                        status=status.HTTP_400_BAD_REQUEST)

    sql = "UPDATE turnos SET estado = %s WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, [nuevo_estado, turno_id])

    return Response({"mensaje": "Estado actualizado correctamente."})


# 6. Cancelar turno
@api_view(["PUT"])
@permission_classes([IsAdmin])
def cancelar_turno(request, turno_id):
    sql = "UPDATE turnos SET estado = 'cancelado' WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(sql, [turno_id])
        if cursor.rowcount == 0:
            return Response({"mensaje": "Turno no encontrado."},
                            status=status.HTTP_404_NOT_FOUND)

    return Response({"mensaje": "Turno cancelado correctamente."})
