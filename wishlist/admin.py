from django.contrib import admin
from .models import WishlistItem

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'fecha_agregado']
    list_filter = ['fecha_agregado', 'usuario']
    search_fields = ['usuario__username', 'producto__nombre']
    date_hierarchy = 'fecha_agregado'
