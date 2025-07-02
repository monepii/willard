from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    """Vista principal de la ferretería"""
    return render(request, 'ferretetia/main.html')

def wishlist(request):
    """Vista de la lista de deseos"""
    context = {
        'page_title': 'Lista de Deseos',
        'wishlist_items': []
    }
    return render(request, 'ferretetia/wishlist.html', context)

def compare(request):
    """Vista de comparación de productos"""
    context = {
        'page_title': 'Comparar Productos',
        'compare_items': []
    }
    return render(request, 'ferretetia/compare.html', context)

def account(request):
    """Vista de mi cuenta"""
    context = {
        'page_title': 'Mi Cuenta',
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'ferretetia/account.html', context)

def checkout(request):
    """Vista de checkout"""
    context = {
        'page_title': 'Finalizar Compra'
    }
    return render(request, 'ferretetia/checkout.html', context)

def cart(request):
    """Vista del carrito de compras"""
    context = {
        'page_title': 'Carrito de Compras',
        'cart_items': [],
        'total': 0
    }
    return render(request, 'ferretetia/cart.html', context)

@csrf_exempt
def search_products(request):
    """API para búsqueda de productos"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            
            # Simulamos resultados de búsqueda
            results = [
                {'id': 1, 'name': f'Martillo - {query}', 'price': 25.99},
                {'id': 2, 'name': f'Destornillador - {query}', 'price': 15.50},
                {'id': 3, 'name': f'Taladro - {query}', 'price': 89.99},
            ] if query else []
            
            return JsonResponse({
                'success': True,
                'results': results,
                'count': len(results)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def power_tools(request):
    """Vista de herramientas eléctricas"""
    context = {
        'page_title': 'Herramientas Eléctricas',
        'products': [
            {'name': 'Taladro Inalámbrico', 'price': 89.99, 'image': 'drill.jpg'},
            {'name': 'Sierra Circular', 'price': 129.99, 'image': 'saw.jpg'},
            {'name': 'Lijadora Orbital', 'price': 65.99, 'image': 'sander.jpg'},
        ]
    }
    return render(request, 'ferretetia/power_tools.html', context)

def blog(request):
    """Vista del blog"""
    context = {
        'page_title': 'Blog de Ferretería',
        'posts': [
            {'title': 'Cómo elegir el martillo correcto', 'date': '2025-07-01'},
            {'title': 'Mantenimiento de herramientas eléctricas', 'date': '2025-06-28'},
        ]
    }
    return render(request, 'ferretetia/blog.html', context)

def shop(request):
    """Vista de la tienda"""
    context = {
        'page_title': 'Tienda',
        'categories': ['Herramientas', 'Materiales', 'Pinturas', 'Electricidad']
    }
    return render(request, 'ferretetia/shop.html', context)

def pages(request):
    """Vista de páginas adicionales"""
    context = {
        'page_title': 'Páginas'
    }
    return render(request, 'ferretetia/pages.html', context)

def elements(request):
    """Vista de elementos"""
    context = {
        'page_title': 'Elementos'
    }
    return render(request, 'ferretetia/elements.html', context)
