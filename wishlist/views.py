from django.shortcuts import render, redirect
from django.contrib import messages

# Lista global para wishlist (en producción usarías sesiones o base de datos)
WISHLIST = []

def wishlist_view(request):
    """Vista de la lista de deseos"""
    context = {
        'page_title': 'Lista de Deseos',
        'wishlist_items': WISHLIST
    }
    return render(request, 'wishlist/wishlist.html', context)

def add_to_wishlist(request, product_id):
    """Agregar producto a la lista de deseos"""
    if product_id not in WISHLIST:
        WISHLIST.append(product_id)
        messages.success(request, "Producto agregado a la lista de deseos.")
    else:
        messages.info(request, "El producto ya está en tu lista de deseos.")
    return redirect('wishlist:wishlist')

def remove_from_wishlist(request, product_id):
    """Eliminar producto de la lista de deseos"""
    if product_id in WISHLIST:
        WISHLIST.remove(product_id)
        messages.success(request, "Producto eliminado de la lista de deseos.")
    else:
        messages.error(request, "Producto no encontrado en la lista de deseos.")
    return redirect('wishlist:wishlist')
