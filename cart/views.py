from django.shortcuts import render, redirect
from django.contrib import messages

# Datos simulados
PRODUCTS = {
    1: {'name': 'Taladro Inalámbrico', 'price': 89.99, 'image': 'drill.jpg'},
    2: {'name': 'Sierra Circular', 'price': 129.99, 'image': 'saw.jpg'},
    3: {'name': 'Lijadora Orbital', 'price': 65.99, 'image': 'sander.jpg'}
}

CART = {}


def cart_view(request):
    """Vista del carrito de compras"""
    total = sum(item['quantity'] * PRODUCTS[item_id]['price'] for item_id, item in CART.items())
    context = {
        'page_title': 'Carrito de Compras',
        'cart_items': CART.items(),
        'total': total
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    """Agregar un producto al carrito"""
    if product_id in PRODUCTS:
        if product_id in CART:
            CART[product_id]['quantity'] += 1
        else:
            CART[product_id] = {'quantity': 1}
        messages.success(request, f"{PRODUCTS[product_id]['name']} ha sido agregado al carrito.")
    else:
        messages.error(request, "Producto inválido.")
    return redirect('cart:cart')

def remove_from_cart(request, product_id):
    """Eliminar un producto del carrito"""
    if product_id in CART:
        del CART[product_id]
        messages.success(request, "Producto eliminado del carrito.")
    else:
        messages.error(request, "Producto no encontrado en el carrito.")
    return redirect('cart:cart')

def update_cart(request, product_id):
    """Actualizar la cantidad de un producto en el carrito"""
    if product_id in CART:
        try:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity >= 1:
                CART[product_id]['quantity'] = new_quantity
                messages.success(request, "Cantidad actualizada.")
            else:
                del CART[product_id]
                messages.success(request, "Producto eliminado del carrito.")
        except ValueError:
            messages.error(request, "Cantidad inválida.")
    else:
        messages.error(request, "Producto no encontrado en el carrito.")
    return redirect('cart:cart')

def clear_cart(request):
    """Limpiar el carrito de compras"""
    CART.clear()
    messages.success(request, "Carrito de compras vacío.")
    return redirect('cart:cart')
