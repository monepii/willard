from django.contrib import admin
from .models import Blog

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha', 'publicado')
    list_filter = ('publicado', 'fecha', 'autor')
    search_fields = ('titulo', 'descripcion', 'contenido')
    list_editable = ('publicado',)
    date_hierarchy = 'fecha'
