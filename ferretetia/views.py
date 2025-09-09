from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .filters import ProductoFilter, CategoriaFilter
from django.db import models

def global_categories(request):
    """Context processor para categorías globales"""
    from .models import Categoria
    categorias = Categoria.objects.filter(activa=True)
    return {'global_categories': categorias}

def index(request):
    """Vista principal de la ferretería"""
    from .models import Producto, Categoria
    from blog.models import Blog
    
    productos = Producto.objects.filter(disponible=True).order_by('-creado')[:12]
    
    # Productos para el carrusel (productos destacados o en oferta)
    productos_carrusel = Producto.objects.filter(
        disponible=True,
        descuento=True
    ).order_by('-creado')[:5]
    
    if not productos_carrusel.exists():
        productos_carrusel = Producto.objects.filter(
            disponible=True
        ).order_by('-creado')[:5]
    
    #  Productos en descuento para la sección de ofertas
    productos_descuento = Producto.objects.filter(
        disponible=True,
        descuento=True
    ).order_by('-creado')[:4]
    
    categorias = Categoria.objects.filter(activa=True).distinct()
    
    blogs = Blog.objects.filter(publicado=True).order_by('-fecha')[:8]
    
    context = {
        "productos": productos,
        "productos_carrusel": productos_carrusel,
        "productos_descuento": productos_descuento,  # ✅
        "categorias": categorias,
        "blogs": blogs
    }
    return render(request, 'ferretetia/main.html', context)


@csrf_exempt
def search_products(request):
    """API para búsqueda de productos en tiempo real"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            
            if query:
                # Buscar productos que coincidan con la consulta
                from .models import Producto
                productos = Producto.objects.filter(
                    models.Q(nombre__icontains=query) |
                    models.Q(descripcion__icontains=query) |
                    models.Q(sku__icontains=query) |
                    models.Q(categoria__nombre__icontains=query)
                ).filter(disponible=True)[:10]  # Limitar a 10 resultados
                
                results = []
                for producto in productos:
                    results.append({
                        'id': producto.id,
                        'name': producto.nombre,
                        'price': float(producto.precio),
                        'sku': producto.sku,
                        'image': producto.imagen.url if producto.imagen else None,
                        'category': producto.categoria.nombre if producto.categoria else None,
                        'url': f'/shop/?search={query}'  # Redirigir a la tienda con filtro
                    })
                
                return JsonResponse({
                    'success': True,
                    'results': results,
                    'count': len(results),
                    'query': query
                })
            else:
                return JsonResponse({
                    'success': True,
                    'results': [],
                    'count': 0,
                    'query': ''
                })
                
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def shop(request):
    """Vista de la tienda con filtros avanzados"""
    from .models import Producto, Categoria
    from .filters import ProductoFilter
    
    # Verificar si hay un parámetro de categoría por nombre
    categoria_nombre = request.GET.get('categoria')
    if categoria_nombre:
        try:
            # Buscar la categoría por nombre
            categoria = Categoria.objects.get(nombre=categoria_nombre, activa=True)
            # Crear un GET modificado con el ID de la categoría
            modified_get = request.GET.copy()
            modified_get['categoria'] = categoria.id
            producto_filter = ProductoFilter(modified_get, queryset=Producto.objects.filter(disponible=True))
        except Categoria.DoesNotExist:
            # Si no se encuentra la categoría, usar filtros normales
            producto_filter = ProductoFilter(request.GET, queryset=Producto.objects.filter(disponible=True))
    else:
        # Verificar si hay un parámetro de búsqueda directo
        search_query = request.GET.get('search')
        if search_query:
            # Si hay búsqueda directa, crear un GET modificado para el filtro
            modified_get = request.GET.copy()
            modified_get['search'] = search_query
            producto_filter = ProductoFilter(modified_get, queryset=Producto.objects.filter(disponible=True))
        else:
            # Aplicar filtros normales
            producto_filter = ProductoFilter(request.GET, queryset=Producto.objects.filter(disponible=True))
    
    productos = producto_filter.qs
    
    # Obtener todas las categorías activas para el sidebar
    categorias = Categoria.objects.filter(activa=True).distinct()
    
    # Contar productos filtrados
    total_productos = productos.count()
    
    context = { 
        'page_title': 'Tienda',
        'categorias': categorias,
        'productos': productos,
        'filter': producto_filter,
        'total_productos': total_productos,
        'filtros_aplicados': any(request.GET.values()),
        'search_query': request.GET.get('search'),
        'categoria_actual': categoria_nombre
    }
    return render(request, 'ferretetia/shop.html', context)


def product_detail(request, product_id):
    """Vista para el detalle de un producto"""
    try:
        producto = Producto.objects.get(id=product_id, disponible=True)
    except Producto.DoesNotExist:
        messages.error(request, "Producto no encontrado")
        return redirect('ferretetia:shop')
    
    context = {
        'producto': producto,
        'page_title': f'{producto.nombre} - WILLARD'
    }
    return render(request, 'ferretetia/product_detail.html', context)


def advanced_search(request):
    """Vista avanzada de búsqueda con filtros"""
    from .models import Producto, Categoria
    from .filters import ProductoFilter, CategoriaFilter
    
    # Filtros de productos
    producto_filter = ProductoFilter(request.GET, queryset=Producto.objects.all())
    productos = producto_filter.qs
    
    # Filtros de categorías
    categoria_filter = CategoriaFilter(request.GET, queryset=Categoria.objects.all())
    categorias = categoria_filter.qs
    
    # Estadísticas
    stats = {
        'total_productos': Producto.objects.count(),
        'productos_filtrados': productos.count(),
        'total_categorias': Categoria.objects.count(),
        'categorias_filtradas': categorias.count(),
        'productos_disponibles': Producto.objects.filter(disponible=True).count(),
        'productos_con_descuento': Producto.objects.filter(descuento=True).count(),
    }
    
    context = {
        'page_title': 'Búsqueda Avanzada',
        'productos': productos,
        'categorias': categorias,
        'producto_filter': producto_filter,
        'categoria_filter': categoria_filter,
        'stats': stats,
        'filtros_aplicados': any(request.GET.values())
    }
    return render(request, 'ferretetia/advanced_search.html', context)


def elements(request):
    """Vista de elementos"""
    context = {
        'page_title': 'Elementos'
    }
    return render(request, 'ferretetia/elements.html', context)

def blog(request):
    """Vista de blog"""
    context = {
        'page_title': 'blog'
    }
    return render(request, 'blog/blog.html', context)


def test_search(request):
    """Vista para probar la búsqueda"""
    return render(request, 'ferretetia/test_search.html')

