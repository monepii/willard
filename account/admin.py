from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_personalizado", "user", "nombre","apellido", "telefono", "email", "direccion", "creado")
    search_fields = ("nombre", "user__username", "email", "id_personalizado")
    list_display_links = ("id_personalizado", "user")
    ordering = ("id_personalizado",)
   