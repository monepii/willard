from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "nombre", "telefono", "email", "direccion", "creado")
    search_fields = ("nombre", "user__username", "email")
   