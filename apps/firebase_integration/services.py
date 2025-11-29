import os
import atexit
import firebase_admin
from firebase_admin import credentials, db
from django.conf import settings
from datetime import datetime


firebase_app = None
firebase_rtdb = None


def initialize_firebase():
    """
    Inicializa Firebase de forma equivalente a firebase.js
    """
    global firebase_app, firebase_rtdb

    if firebase_app:
        return firebase_rtdb

    cred_path = os.path.join(settings.BASE_DIR, settings.FIREBASE_CREDENTIALS)

    if not os.path.exists(cred_path):
        print(f"[FIREBASE] No se encontró credencial: {cred_path}")
        return None

    try:
        cred = credentials.Certificate(cred_path)

        firebase_app = firebase_admin.initialize_app(
            cred,
            {"databaseURL": settings.FIREBASE_DATABASE_URL}
        )

        firebase_rtdb = db
        print("[FIREBASE] RTDB inicializada correctamente")

        # Marcar servidor online (equivalente a Node)
        mark_server_online()

        # Registrar apagado limpio
        atexit.register(mark_server_offline)

        return firebase_rtdb

    except Exception as e:
        print("[FIREBASE] Error al inicializar:", e)
        return None


# ===========================================================
# Funciones equivalentes a Node.js
# ===========================================================

def mark_server_online():
    """
    rtdb.ref('servidor/estado').set(...)
    """
    rtdb = initialize_firebase()
    if not rtdb:
        return

    try:
        rtdb.reference("servidor/estado").set({
            "online": True,
            "hora": datetime.utcnow().isoformat()
        })
        print("[FIREBASE] servidor/estado = online")
    except Exception as e:
        print("[FIREBASE] No se pudo marcar online:", e)


def mark_server_offline():
    """
    rtdb.ref('servidor/estado').update(...)
    """
    rtdb = initialize_firebase()
    if not rtdb:
        return

    try:
        rtdb.reference("servidor/estado").update({
            "online": False,
            "hora": datetime.utcnow().isoformat()
        })
        print("[FIREBASE] servidor/estado = offline")
    except:
        pass


# ===========================================================
# Helpers equivalentes: set, update, push, get
# ===========================================================

def firebase_set(path: str, data):
    rtdb = initialize_firebase()
    if not rtdb:
        return None
    ref = rtdb.reference(path)
    ref.set(data)
    return True


def firebase_update(path: str, data):
    rtdb = initialize_firebase()
    if not rtdb:
        return None
    ref = rtdb.reference(path)
    ref.update(data)
    return True


def firebase_push(path: str, data):
    rtdb = initialize_firebase()
    if not rtdb:
        return None
    ref = rtdb.reference(path)
    new_ref = ref.push(data)
    return new_ref.key


def firebase_get(path: str):
    rtdb = initialize_firebase()
    if not rtdb:
        return None
    ref = rtdb.reference(path)
    return ref.get()
