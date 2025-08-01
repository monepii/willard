from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def global_categories(request):
    """Context processor to make categories available globally"""
    try:
        from .models import Categoria
        categorias = Categoria.objects.filter(activa=True).distinct()
        return {'global_categorias': list(categorias)}
    except Exception as e:
        return {'global_categorias': []}

def index(request):
    """Vista principal de la ferretería"""
    from .models import Producto, Categoria
    
    productos = Producto.objects.filter(disponible=True).order_by('-creado')[:12]
    
    # Obtener categorías para el dropdown
    categorias = Categoria.objects.filter(activa=True).distinct()
    
    context = {
        "productos": productos,
        "categorias": categorias
    }
    return render(request, 'ferretetia/main.html', context)


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
    from .models import Producto, Categoria
    
    # Filtrar por categoría si se especifica
    categoria_filtro = request.GET.get('categoria')
    if categoria_filtro:
        productos = Producto.objects.filter(
            disponible=True, 
            categoria__nombre__icontains=categoria_filtro
        ).order_by('-creado')
    else:
        productos = Producto.objects.filter(disponible=True).order_by('-creado')
    
    # Obtener todas las categorías activas
    categorias = Categoria.objects.filter(activa=True).distinct()
    context = { 
        'page_title': 'Tienda',
        'categorias': categorias,
        'productos': productos,
        'categoria_actual': categoria_filtro
    }
    return render(request, 'ferretetia/shop.html', context)


def elements(request):
    """Vista de elementos"""
    context = {
        'page_title': 'Elementos'
    }
    return render(request, 'ferretetia/elements.html', context)

def account(request):
    """Vista de cuenta"""
    context = {
        'page_title': 'Account'
    }
    return render(request, 'account/account.html', context)

def wishlist(request):
    """Vista de wishlist"""
    context = {
        'page_title': 'Wishlist'
    }
    return render(request, 'wishlist/wishlist.html', context)


def compare(request):
    """Vista de comparar"""
    context = {
        'page_title': 'Compare'
    }
    return render(request, 'compare/compare.html', context)


def checkout(request):
    """Vista de checkout"""
    context = {
        'page_title': 'checkout'
    }
    return render(request, 'checkout/checkout.html', context)

def cart(request):
    """Vista de carrito"""
    context = {
        'page_title': 'Cart'
    }
    return render(request, 'cart/cart.html', context)






