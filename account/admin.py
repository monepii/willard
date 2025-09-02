from django.contrib import admin
from .models import PerfilUsuario, Direccion

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_personalizado", "user", "nombre","apellido", "telefono", "email", "direccion", "creado")
    search_fields = ("nombre", "user__username", "email", "id_personalizado")
    list_display_links = ("id_personalizado", "user")
    ordering = ("id_personalizado",)

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ("user", "calle", "numero_exterior", "colonia", "municipio", "estado", "es_principal", "activa", "creada")
    search_fields = ("user__username", "calle", "colonia", "municipio", "estado")
    list_filter = ("estado", "municipio", "es_principal", "activa", "creada")
    list_display_links = ("user", "calle")
    ordering = ("-es_principal", "-creada")
    list_editable = ("es_principal", "activa")
   