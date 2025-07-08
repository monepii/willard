from django.shortcuts import render, redirect
from django.contrib import messages

# Lista global para comparar productos (en producción usarías sesiones o base de datos)
COMPARE_LIST = []

def compare_view(request):
    """Vista de comparación de productos"""
    context = {
        'page_title': 'Comparar Productos',
        'compare_items': COMPARE_LIST
    }
    return render(request, 'compare/compare.html', context)

def add_to_compare(request, product_id):
    """Agregar producto a comparación"""
    if len(COMPARE_LIST) < 4:  # Límite de 4 productos para comparar
        if product_id not in COMPARE_LIST:
            COMPARE_LIST.append(product_id)
            messages.success(request, "Producto agregado a comparación.")
        else:
            messages.info(request, "El producto ya está en la lista de comparación.")
    else:
        messages.error(request, "Solo puedes comparar hasta 4 productos.")
    return redirect('compare:compare')

def remove_from_compare(request, product_id):
    """Eliminar producto de comparación"""
    if product_id in COMPARE_LIST:
        COMPARE_LIST.remove(product_id)
        messages.success(request, "Producto eliminado de la comparación.")
    else:
        messages.error(request, "Producto no encontrado en la lista de comparación.")
    return redirect('compare:compare')
