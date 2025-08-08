#!/usr/bin/env python
"""
Script simple para probar las URLs de categorías
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from ferretetia.models import Categoria
from django.urls import reverse

def test_urls():
    """Probar las URLs de categorías"""
    
    print("=== PRUEBA DE URLs DE CATEGORÍAS ===")
    
    # Obtener categorías
    categorias = Categoria.objects.filter(activa=True)
    
    for categoria in categorias:
        # Generar URL
        url = f"/shop/?categoria={categoria.nombre}"
        print(f"Categoría: {categoria.nombre}")
        print(f"URL: {url}")
        print(f"Productos en esta categoría: {categoria.productos.filter(disponible=True).count()}")
        print("-" * 50)

if __name__ == '__main__':
    test_urls()
