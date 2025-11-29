from .services import firebase_push, firebase_set, firebase_update, firebase_get

def registrar_log(usuario_id, accion):
    firebase_push("logs", {
        "usuario": usuario_id,
        "accion": accion
    })

def notificar_turno(paciente_id, mensaje):
    firebase_push(f"notificaciones/paciente/{paciente_id}", {
        "mensaje": mensaje
    })
