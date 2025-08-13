from django.contrib import admin
from django_filters import AllValuesFilter, ChoiceFilter
from .models import Producto, Categoria
from .filters import ProductoFilter


class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "disponible", "creado")
    search_fields = ("nombre", "categoria__nombre", "sku")
    list_filter = ("disponible", "creado", "categoria", "descuento")
    list_editable = ("precio", "stock", "disponible")
    readonly_fields = ("creado", "actualizado")
    
    # Campos para edición rápida
    list_per_page = 25
    
    # Campos para el formulario de edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('sku', 'nombre', 'descripcion', 'categoria')
        }),
        ('Precios y Stock', {
            'fields': ('precio', 'descuento', 'precioDescuento', 'stock')
        }),
        ('Estado', {
            'fields': ('disponible',)
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
        ('Fechas', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa", "productos_count", "creado")
    list_filter = ("activa", "creado")
    search_fields = ("nombre", "descripcion")
    list_editable = ("activa",)
    readonly_fields = ("creado", "actualizado")
    
    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = "Productos"
    productos_count.admin_order_field = 'productos__count'


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
