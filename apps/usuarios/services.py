import requests
from django.conf import settings

def enviar_correo_alta(nombre, email):
    try:
        url = "https://us-central1-salud-total-a0d92.cloudfunctions.net/correos-correoAltaUsuario"
        requests.post(url, {
            "nombre": nombre,
            "email": email,
            "tipo": "paciente"
        })
    except Exception as e:
        print("ERROR enviando correo:", e)

def sync_paciente_firebase(rtdb, user_id, data):
    if not rtdb:
        return
    try:
        ref = rtdb.ref(f"usuarios/pacientes/{user_id}")
        ref.set(data)
    except Exception as e:
        print("Error Firebase:", e)
