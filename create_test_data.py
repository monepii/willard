#!/usr/bin/env python
"""
Script para crear datos de prueba para la ferretería
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from ferretetia.models import Categoria, Producto

def create_test_data():
    """Crear datos de prueba"""
    
    # Crear categorías
    categorias = [
        {
            'nombre': 'Herramientas Manuales',
            'descripcion': 'Martillos, destornilladores, alicates y más herramientas manuales'
        },
        {
            'nombre': 'Herramientas Eléctricas',
            'descripcion': 'Taladros, sierras, lijadoras y herramientas eléctricas profesionales'
        },
        {
            'nombre': 'Pinturas y Accesorios',
            'descripcion': 'Pinturas, brochas, rodillos y accesorios para pintura'
        },
        {
            'nombre': 'Plomería',
            'descripcion': 'Tuberías, válvulas, conexiones y accesorios de plomería'
        }
    ]
    
    for cat_data in categorias:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion']}
        )
        if created:
            print(f"Categoría creada: {categoria.nombre}")
    
    # Crear productos
    productos = [
        {
            'sku': 'MART-001',
            'nombre': 'Martillo de Carpintero',
            'descripcion': 'Martillo profesional de 16 oz con mango de fibra de vidrio',
            'categoria': 'Herramientas Manuales',
            'precio': 25.99,
            'stock': 50,
            'descuento': False
        },
        {
            'sku': 'DEST-001',
            'nombre': 'Destornillador Phillips',
            'descripcion': 'Destornillador Phillips #2 con mango ergonómico',
            'categoria': 'Herramientas Manuales',
            'precio': 12.50,
            'stock': 100,
            'descuento': True,
            'precioDescuento': 9.99
        },
        {
            'sku': 'TAL-001',
            'nombre': 'Taladro Inalámbrico',
            'descripcion': 'Taladro inalámbrico 20V con batería de litio incluida',
            'categoria': 'Herramientas Eléctricas',
            'precio': 89.99,
            'stock': 25,
            'descuento': False
        },
        {
            'sku': 'SIER-001',
            'nombre': 'Sierra Circular',
            'descripcion': 'Sierra circular de 7-1/4" con motor de 15 amperios',
            'categoria': 'Herramientas Eléctricas',
            'precio': 129.99,
            'stock': 15,
            'descuento': True,
            'precioDescuento': 109.99
        },
        {
            'sku': 'PINT-001',
            'nombre': 'Pintura Interior Blanca',
            'descripcion': 'Pintura interior blanca de 1 galón, acabado satinado',
            'categoria': 'Pinturas y Accesorios',
            'precio': 35.99,
            'stock': 75,
            'descuento': False
        },
        {
            'sku': 'BRO-001',
            'nombre': 'Brocha de 2"',
            'descripcion': 'Brocha profesional de 2" con cerdas naturales',
            'categoria': 'Pinturas y Accesorios',
            'precio': 8.99,
            'stock': 200,
            'descuento': False
        },
        {
            'sku': 'TUB-001',
            'nombre': 'Tubería PVC 1"',
            'descripcion': 'Tubería PVC de 1" x 10 pies para drenaje',
            'categoria': 'Plomería',
            'precio': 15.99,
            'stock': 60,
            'descuento': False
        },
        {
            'sku': 'VAL-001',
            'nombre': 'Válvula de Compuerta 1/2"',
            'descripcion': 'Válvula de compuerta de latón de 1/2"',
            'categoria': 'Plomería',
            'precio': 22.50,
            'stock': 40,
            'descuento': True,
            'precioDescuento': 18.99
        }
    ]
    
    for prod_data in productos:
        categoria = Categoria.objects.get(nombre=prod_data['categoria'])
        
        producto, created = Producto.objects.get_or_create(
            sku=prod_data['sku'],
            defaults={
                'nombre': prod_data['nombre'],
                'descripcion': prod_data['descripcion'],
                'categoria': categoria,
                'precio': prod_data['precio'],
                'stock': prod_data['stock'],
                'descuento': prod_data.get('descuento', False),
                'precioDescuento': prod_data.get('precioDescuento', None)
            }
        )
        
        if created:
            print(f"Producto creado: {producto.nombre} - ${producto.precio}")
        else:
            print(f"Producto ya existe: {producto.nombre}")

if __name__ == '__main__':
    print("Creando datos de prueba...")
    create_test_data()
    print("¡Datos de prueba creados exitosamente!") 