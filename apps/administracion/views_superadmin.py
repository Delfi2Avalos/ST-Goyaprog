from rest_framework.views import APIView
from rest_framework.response import Response
from apps.administracion.permissions import IsSuperAdmin
from apps.administracion.serializers import SuperAdminSerializer
from apps.administracion.services import SuperAdminActions

class CrearSuperAdminView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        usuario = SuperAdminActions.crear_superadmin(request.data)
        return Response(SuperAdminSerializer(usuario).data, status=201)

class ListarAdminsView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        admins = SuperAdminActions.listar_admins()
        serializer = SuperAdminSerializer(admins, many=True)
        return Response(serializer.data)
