from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ferretetia.models import Producto


def get_compare_list(request):
    """Obtener la lista de comparación de la sesión"""
    return request.session.get('compare_list', [])


def set_compare_list(request, compare_list):
    """Guardar la lista de comparación en la sesión"""
    request.session['compare_list'] = compare_list
    request.session.modified = True


def compare_view(request):
    """Vista de comparación de productos"""
    compare_list = get_compare_list(request)
    
    # Obtener los productos completos
    productos = Producto.objects.filter(id__in=compare_list).select_related('categoria', 'subcategoria')
    
    # Agrupar productos por subcategoría
    productos_por_subcategoria = {}
    productos_sin_subcategoria = []
    
    for producto in productos:
        if producto.subcategoria:
            subcat_id = producto.subcategoria.id
            if subcat_id not in productos_por_subcategoria:
                productos_por_subcategoria[subcat_id] = {
                    'subcategoria': producto.subcategoria,
                    'productos': []
                }
            productos_por_subcategoria[subcat_id]['productos'].append(producto)
        else:
            productos_sin_subcategoria.append(producto)
    
    # Verificar si todos los productos son de la misma subcategoría
    puede_comparar = len(productos_por_subcategoria) <= 1 and len(productos_sin_subcategoria) == 0
    
    context = {
        'page_title': 'Comparar Productos',
        'productos': productos,
        'productos_por_subcategoria': productos_por_subcategoria,
        'productos_sin_subcategoria': productos_sin_subcategoria,
        'puede_comparar': puede_comparar,
        'total_productos': len(productos),
    }
    return render(request, 'compare/compare.html', context)


def add_to_compare(request, product_id):
    """Agregar producto a comparación"""
    compare_list = get_compare_list(request)
    producto = get_object_or_404(Producto, id=product_id)
    
    # Verificar si ya hay productos en la lista
    if compare_list:
        # Obtener los productos actuales
        productos_actuales = Producto.objects.filter(id__in=compare_list).select_related('subcategoria')
        
        # Verificar si todos tienen subcategoría
        if not producto.subcategoria:
            messages.error(request, "Solo puedes comparar productos que tengan subcategoría asignada.")
            return redirect(request.META.get('HTTP_REFERER', 'ferretetia:index'))
        
        # Verificar que todos los productos actuales tengan la misma subcategoría
        subcategoria_actual = productos_actuales.first().subcategoria if productos_actuales else None
        
        if subcategoria_actual and producto.subcategoria.id != subcategoria_actual.id:
            messages.error(
                request, 
                f"Solo puedes comparar productos de la misma subcategoría. "
                f"Los productos actuales son de '{subcategoria_actual.nombre}', "
                f"pero el producto seleccionado es de '{producto.subcategoria.nombre}'."
            )
            return redirect(request.META.get('HTTP_REFERER', 'ferretetia:index'))
    
    # Verificar límite de productos
    if len(compare_list) >= 4:
        messages.error(request, "Solo puedes comparar hasta 4 productos.")
        return redirect(request.META.get('HTTP_REFERER', 'ferretetia:index'))
    
    # Verificar si el producto ya está en la lista
    if product_id in compare_list:
        messages.info(request, "El producto ya está en la lista de comparación.")
    else:
        compare_list.append(product_id)
        set_compare_list(request, compare_list)
        messages.success(request, f"'{producto.nombre}' agregado a comparación.")
    
    return redirect(request.META.get('HTTP_REFERER', 'ferretetia:index'))


def remove_from_compare(request, product_id):
    """Eliminar producto de comparación"""
    compare_list = get_compare_list(request)
    
    if product_id in compare_list:
        compare_list.remove(product_id)
        set_compare_list(request, compare_list)
        messages.success(request, "Producto eliminado de la comparación.")
    else:
        messages.error(request, "Producto no encontrado en la lista de comparación.")
    
    return redirect('compare:compare')


def clear_compare(request):
    """Limpiar toda la lista de comparación"""
    request.session['compare_list'] = []
    request.session.modified = True
    messages.success(request, "Lista de comparación limpiada.")
    return redirect('compare:compare')
