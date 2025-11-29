from apps.usuarios.models import Usuario

class AdminActions:

    @staticmethod
    def crear_admin(data):
        data["tipo"] = "admin"
        usuario = Usuario.objects.create_user(**data)
        return usuario

    @staticmethod
    def listar_medicos():
        return Usuario.objects.filter(tipo="medico")

class SuperAdminActions:

    @staticmethod
    def crear_superadmin(data):
        data["tipo"] = "superadmin"
        usuario = Usuario.objects.create_user(**data)
        return usuario

    @staticmethod
    def listar_admins():
        return Usuario.objects.filter(tipo="admin")
