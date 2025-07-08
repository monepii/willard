from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    """Vista principal de la ferretería"""
    from .models import Producto
    productos = Producto.objects.filter(disponible=True).order_by('-creado')
    return render(request, 'ferretetia/main.html', {"productos": productos})


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


def shop(request):
    """Vista de la tienda"""
    context = {
        'page_title': 'Tienda',
        'categories': ['Herramientas', 'Materiales', 'Pinturas', 'Electricidad']
    }
    return render(request, 'ferretetia/shop.html', context)


def elements(request):
    """Vista de elementos"""
    context = {
        'page_title': 'Elementos'
    }
    return render(request, 'ferretetia/elements.html', context)
