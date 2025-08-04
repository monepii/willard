from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Carrito, ItemCarrito
from ferretetia.models import Producto


def cart_view(request):
    """Vista del carrito de compras"""
    carrito = Carrito.obtener_o_crear_carrito(request)
    items = carrito.items.all()
    
    # Calcular el total del carrito
    total_precio = carrito.total_precio
    
    context = {
        'page_title': 'Carrito de Compras',
        'carrito': carrito,
        'items': items,
        'total_items': carrito.total_items,
        'total_precio': total_precio,
        'cart_is_empty': carrito.total_items == 0
    }
    
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    """Agregar un producto al carrito"""
    try:
        producto = get_object_or_404(Producto, id=product_id, disponible=True)
        carrito = Carrito.obtener_o_crear_carrito(request)
        

        
        # Verificar si el producto ya está en el carrito
        try:
            item = ItemCarrito.objects.get(carrito=carrito, producto=producto)
            # Si ya existe, aumentar la cantidad
            nueva_cantidad = item.cantidad + 1
            if nueva_cantidad <= producto.stock:
                item.cantidad = nueva_cantidad
                # Actualizar el precio unitario antes de guardar
                item.actualizar_precio()
                item.save()

                messages.success(request, f"Cantidad de {producto.nombre} actualizada en el carrito.")
            else:
                messages.error(request, f"No hay suficiente stock disponible. Máximo: {producto.stock}")
        except ItemCarrito.DoesNotExist:
            # Si no existe, crear nuevo item
            if producto.stock > 0:
                # Determinar el precio unitario
                if producto.descuento and producto.precioDescuento:
                    precio_unitario = producto.precioDescuento
                else:
                    precio_unitario = producto.precio
                
                item = ItemCarrito.objects.create(
                    carrito=carrito,
                    producto=producto,
                    cantidad=1,
                    precio_unitario=precio_unitario
                )

                messages.success(request, f"{producto.nombre} ha sido agregado al carrito.")
            else:
                messages.error(request, "Producto sin stock disponible.")
        

        
    except Producto.DoesNotExist:
        messages.error(request, "Producto no encontrado o no disponible.")
    except Exception as e:
        messages.error(request, f"Error al agregar el producto: {str(e)}")
    
    return redirect('cart:cart')


def remove_from_cart(request, item_id):
    """Eliminar un item del carrito"""
    try:
        carrito = Carrito.obtener_o_crear_carrito(request)
        item = get_object_or_404(ItemCarrito, id=item_id, carrito=carrito)
        producto_nombre = item.producto.nombre
        item.delete()
        messages.success(request, f"{producto_nombre} ha sido eliminado del carrito.")
    except ItemCarrito.DoesNotExist:
        messages.error(request, "Item no encontrado en el carrito.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el item: {str(e)}")
    
    return redirect('cart:cart')


def update_cart(request, item_id):
    """Actualizar la cantidad de un item en el carrito"""
    if request.method == 'POST':
        try:
            carrito = Carrito.obtener_o_crear_carrito(request)
            item = get_object_or_404(ItemCarrito, id=item_id, carrito=carrito)
            nueva_cantidad = int(request.POST.get('cantidad', 1))
            
            if nueva_cantidad > 0:
                # Verificar stock disponible
                if nueva_cantidad <= item.producto.stock:
                    item.cantidad = nueva_cantidad
                    # Actualizar el precio unitario antes de guardar
                    item.actualizar_precio()
                    item.save()
                    messages.success(request, f"Cantidad de {item.producto.nombre} actualizada.")
                else:
                    messages.error(request, f"No hay suficiente stock disponible. Máximo: {item.producto.stock}")
            else:
                # Si la cantidad es 0 o menor, eliminar el item
                item.delete()
                messages.success(request, f"{item.producto.nombre} ha sido eliminado del carrito.")
                
        except ValueError:
            messages.error(request, "Cantidad inválida.")
        except ItemCarrito.DoesNotExist:
            messages.error(request, "Item no encontrado en el carrito.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el carrito: {str(e)}")
    
    return redirect('cart:cart')


def clear_cart(request):
    """Limpiar el carrito de compras"""
    try:
        carrito = Carrito.obtener_o_crear_carrito(request)
        carrito.limpiar()
        messages.success(request, "Carrito de compras vacío.")
    except Exception as e:
        messages.error(request, f"Error al limpiar el carrito: {str(e)}")
    
    return redirect('cart:cart')


def cart_count(request):
    """API para obtener el número de items en el carrito (para AJAX)"""
    try:
        carrito = Carrito.obtener_o_crear_carrito(request)
        return JsonResponse({
            'success': True,
            'count': carrito.total_items
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def merge_cart(request):
    """Fusionar carrito de sesión con carrito de usuario al hacer login"""
    if request.user.is_authenticated and request.session.session_key:
        try:
            # Obtener carrito de sesión
            session_cart = Carrito.objects.filter(
                session_key=request.session.session_key,
                activo=True
            ).first()
            
            if session_cart:
                # Obtener o crear carrito de usuario
                user_cart, created = Carrito.objects.get_or_create(
                    usuario=request.user,
                    activo=True
                )
                
                # Mover items de sesión a usuario
                for item in session_cart.items.all():
                    existing_item = user_cart.items.filter(producto=item.producto).first()
                    if existing_item:
                        existing_item.cantidad += item.cantidad
                        existing_item.save()
                    else:
                        item.carrito = user_cart
                        item.save()
                
                # Desactivar carrito de sesión
                session_cart.activo = False
                session_cart.save()
                
                messages.success(request, "Tu carrito ha sido actualizado.")
                
        except Exception as e:
            messages.error(request, f"Error al fusionar carritos: {str(e)}")
    
    return redirect('cart:cart')
