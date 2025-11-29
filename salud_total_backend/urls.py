from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de usuarios
    path('api/usuarios/', include('apps.usuarios.urls')),
]
