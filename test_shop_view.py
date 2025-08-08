#!/usr/bin/env python
"""
Script para probar la vista de shop
"""
import os
import sys
import django
from django.test import RequestFactory
from django.urls import reverse

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from ferretetia.views import shop
from ferretetia.models import Categoria

def test_shop_view():
    """Probar la vista de shop con diferentes parámetros"""
    
    factory = RequestFactory()
    
    print("=== PRUEBA DE LA VISTA SHOP ===")
    
    # Probar sin parámetros
    print("\n1. Probando sin parámetros:")
    request = factory.get('/shop/')
    response = shop(request)
    print(f"Status: {response.status_code}")
    
    # Probar con categoría específica
    categoria = Categoria.objects.filter(activa=True).first()
    if categoria:
        print(f"\n2. Probando con categoría: {categoria.nombre}")
        request = factory.get(f'/shop/?categoria={categoria.nombre}')
        response = shop(request)
        print(f"Status: {response.status_code}")
        
        # Verificar si la respuesta contiene productos
        if hasattr(response, 'context_data'):
            productos = response.context_data.get('productos', [])
            print(f"Productos encontrados: {len(productos)}")
    
    # Probar con categoría inexistente
    print("\n3. Probando con categoría inexistente:")
    request = factory.get('/shop/?categoria=CategoriaInexistente')
    response = shop(request)
    print(f"Status: {response.status_code}")

if __name__ == '__main__':
    test_shop_view()
