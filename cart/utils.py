from .models import Carrito, ItemCarrito
from ferretetia.models import Producto


def get_cart(request):
    """Función helper para obtener el carrito del usuario"""
    return Carrito.obtener_o_crear_carrito(request)


def get_cart_items(request):
    """Función helper para obtener los items del carrito"""
    carrito = get_cart(request)
    return carrito.items.all()


def get_cart_total(request):
    """Función helper para obtener el total del carrito"""
    carrito = get_cart(request)
    return carrito.total_precio


def get_cart_count(request):
    """Función helper para obtener el número de items en el carrito"""
    carrito = get_cart(request)
    return carrito.total_items


def add_product_to_cart(request, product_id, quantity=1):
    """Función helper para agregar un producto al carrito"""
    try:
        producto = Producto.objects.get(id=product_id, disponible=True)
        carrito = get_cart(request)
        
        # Verificar stock
        if quantity > producto.stock:
            return False, f"No hay suficiente stock. Disponible: {producto.stock}"
        
        # Verificar si el producto ya está en el carrito
        item, created = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': quantity}
        )
        
        if not created:
            # Si ya existe, verificar que no exceda el stock
            nueva_cantidad = item.cantidad + quantity
            if nueva_cantidad > producto.stock:
                return False, f"No hay suficiente stock. Disponible: {producto.stock}"
            item.cantidad = nueva_cantidad
            item.save()
        
        return True, f"{producto.nombre} agregado al carrito"
        
    except Producto.DoesNotExist:
        return False, "Producto no encontrado"
    except Exception as e:
        return False, f"Error: {str(e)}"


def update_cart_item(request, item_id, quantity):
    """Función helper para actualizar la cantidad de un item"""
    try:
        carrito = get_cart(request)
        item = ItemCarrito.objects.get(id=item_id, carrito=carrito)
        
        if quantity <= 0:
            item.delete()
            return True, "Item eliminado del carrito"
        
        if quantity > item.producto.stock:
            return False, f"No hay suficiente stock. Disponible: {item.producto.stock}"
        
        item.cantidad = quantity
        item.save()
        return True, "Cantidad actualizada"
        
    except ItemCarrito.DoesNotExist:
        return False, "Item no encontrado"
    except Exception as e:
        return False, f"Error: {str(e)}"


def remove_cart_item(request, item_id):
    """Función helper para eliminar un item del carrito"""
    try:
        carrito = get_cart(request)
        item = ItemCarrito.objects.get(id=item_id, carrito=carrito)
        producto_nombre = item.producto.nombre
        item.delete()
        return True, f"{producto_nombre} eliminado del carrito"
        
    except ItemCarrito.DoesNotExist:
        return False, "Item no encontrado"
    except Exception as e:
        return False, f"Error: {str(e)}"


def clear_cart(request):
    """Función helper para limpiar el carrito"""
    try:
        carrito = get_cart(request)
        carrito.limpiar()
        return True, "Carrito vacío"
    except Exception as e:
        return False, f"Error: {str(e)}"


def is_cart_empty(request):
    """Función helper para verificar si el carrito está vacío"""
    carrito = get_cart(request)
    return carrito.total_items == 0


def get_cart_summary(request):
    """Función helper para obtener un resumen del carrito"""
    carrito = get_cart(request)
    return {
        'total_items': carrito.total_items,
        'total_precio': carrito.total_precio,
        'items': carrito.items.all(),
        'is_empty': carrito.total_items == 0
    } 