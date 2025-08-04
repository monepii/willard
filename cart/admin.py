from django.contrib import admin
from .models import Carrito, ItemCarrito


class ItemCarritoInline(admin.TabularInline):
    """Inline para mostrar items del carrito en el admin"""
    model = ItemCarrito
    extra = 0
    readonly_fields = ['precio_unitario', 'precio_total', 'creado', 'actualizado']
    fields = ['producto', 'cantidad', 'precio_unitario', 'precio_total']


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Carrito"""
    list_display = ['id', 'usuario', 'session_key', 'total_items', 'total_precio', 'activo', 'creado']
    list_filter = ['activo', 'creado', 'usuario']
    search_fields = ['usuario__username', 'session_key']
    readonly_fields = ['total_items', 'total_precio', 'creado', 'actualizado']
    inlines = [ItemCarritoInline]
    
    fieldsets = (
        ('Información del Carrito', {
            'fields': ('usuario', 'session_key', 'activo')
        }),
        ('Información de Tiempo', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
        ('Resumen', {
            'fields': ('total_items', 'total_precio'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo ItemCarrito"""
    list_display = ['id', 'carrito', 'producto', 'cantidad', 'precio_unitario', 'precio_total', 'creado']
    list_filter = ['creado', 'producto__categoria']
    search_fields = ['producto__nombre', 'carrito__usuario__username']
    readonly_fields = ['precio_unitario', 'precio_total', 'creado', 'actualizado']
    
    fieldsets = (
        ('Información del Item', {
            'fields': ('carrito', 'producto', 'cantidad')
        }),
        ('Precios', {
            'fields': ('precio_unitario', 'precio_total')
        }),
        ('Información de Tiempo', {
            'fields': ('creado', 'actualizado'),
            'classes': ('collapse',)
        }),
    )
