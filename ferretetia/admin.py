from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "disponible", "creado")
    search_fields = ("nombre", "categoria__nombre")
    list_filter = ("disponible", "creado", "categoria")

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa", "creado")
    search_fields = ("nombre",)
    list_filter = ("activa",)
