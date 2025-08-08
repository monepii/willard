#!/usr/bin/env python
"""
Script para verificar las imágenes de las categorías
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from ferretetia.models import Categoria

def check_category_images():
    """Verificar las imágenes de las categorías"""
    
    print("=== VERIFICACIÓN DE IMÁGENES DE CATEGORÍAS ===")
    
    categorias = Categoria.objects.filter(activa=True)
    
    for categoria in categorias:
        print(f"Categoría: {categoria.nombre}")
        print(f"Tiene imagen: {categoria.imagen is not None}")
        if categoria.imagen:
            print(f"URL de imagen: {categoria.imagen.url}")
            print(f"Ruta de imagen: {categoria.imagen.path}")
            print(f"Existe archivo: {os.path.exists(categoria.imagen.path)}")
        else:
            print("NO TIENE IMAGEN")
        print("-" * 50)

if __name__ == '__main__':
    check_category_images()
