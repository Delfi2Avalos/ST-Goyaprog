from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de usuarios
    path('api/usuarios/', include('apps.usuarios.urls')),

    # Rutas de Administrador
    path('api/admin/', include('apps.administracion.urls')),

    # Rutas de SuperAdmin
    path('api/superadmin/', include('apps.administracion.urls_superadmin')),
]
