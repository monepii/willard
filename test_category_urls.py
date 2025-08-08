#!/usr/bin/env python
"""
Script para probar las URLs de categorías
"""
import os
import sys
import django
import webbrowser
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from ferretetia.models import Categoria

def test_category_urls():
    """Probar las URLs de categorías en el navegador"""
    
    print("=== PRUEBA DE URLs DE CATEGORÍAS EN NAVEGADOR ===")
    
    # URL base del servidor
    base_url = "http://127.0.0.1:8000"
    
    # Obtener categorías
    categorias = Categoria.objects.filter(activa=True)
    
    print("Abriendo URLs en el navegador...")
    print("Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:8000")
    print("-" * 50)
    
    for i, categoria in enumerate(categorias):
        url = f"{base_url}/shop/?categoria={categoria.nombre}"
        print(f"{i+1}. {categoria.nombre}: {url}")
        
        # Abrir en navegador
        webbrowser.open(url)
        time.sleep(1)  # Esperar 1 segundo entre cada apertura
    
    print("\nTodas las URLs han sido abiertas en el navegador.")
    print("Verifica que cada categoría muestre los productos correctos.")

if __name__ == '__main__':
    test_category_urls()
