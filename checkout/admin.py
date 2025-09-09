from django.contrib import admin
from .models import Orden, ItemOrden


class ItemOrdenInline(admin.TabularInline):
    model = ItemOrden
    extra = 0
    readonly_fields = ('precio_total',)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = [
        'numero_orden', 'usuario', 'nombre_completo', 
        'total', 'estado', 'creado'
    ]
    list_filter = ['estado', 'creado', 'actualizado']
    search_fields = ['numero_orden', 'usuario__username', 'nombre_completo', 'email']
    readonly_fields = ['numero_orden', 'creado', 'actualizado']
    
    fieldsets = [
        ('Información General', {
            'fields': ['numero_orden', 'usuario', 'estado']
        }),
        ('Información de Envío', {
            'fields': [
                'nombre_completo', 'email', 'direccion', 
                'ciudad', 'codigo_postal', 'telefono'
            ]
        }),
        ('Totales', {
            'fields': ['subtotal', 'impuestos', 'envio', 'total']
        }),
        ('Fechas', {
            'fields': ['creado', 'actualizado']
        }),
        ('Notas', {
            'fields': ['notas']
        })
    ]
    
    inlines = [ItemOrdenInline]


@admin.register(ItemOrden)
class ItemOrdenAdmin(admin.ModelAdmin):
    list_display = ['orden', 'producto', 'cantidad', 'precio_unitario', 'precio_total']
    list_filter = ['orden__estado', 'orden__creado']
    search_fields = ['orden__numero_orden', 'producto__nombre']
