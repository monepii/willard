#!/usr/bin/env python
"""
Script para verificar las categorías en la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from ferretetia.models import Categoria, Producto

def check_categories():
    """Verificar categorías y productos"""
    
    print("=== VERIFICACIÓN DE CATEGORÍAS ===")
    
    # Verificar categorías
    categorias = Categoria.objects.filter(activa=True)
    print(f"Total de categorías activas: {categorias.count()}")
    
    for categoria in categorias:
        productos_count = Producto.objects.filter(categoria=categoria, disponible=True).count()
        print(f"- {categoria.nombre}: {productos_count} productos")
    
    # Verificar productos sin categoría
    productos_sin_categoria = Producto.objects.filter(categoria__isnull=True, disponible=True)
    print(f"\nProductos sin categoría: {productos_sin_categoria.count()}")
    
    # Verificar todos los productos
    total_productos = Producto.objects.filter(disponible=True).count()
    print(f"Total de productos disponibles: {total_productos}")
    
    # Verificar URLs de ejemplo
    print("\n=== URLs DE EJEMPLO ===")
    for categoria in categorias[:3]:  # Solo las primeras 3
        url = f"/shop/?categoria={categoria.nombre}"
        print(f"URL para {categoria.nombre}: {url}")

if __name__ == '__main__':
    check_categories()
