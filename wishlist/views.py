from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import WishlistItem
from ferretetia.models import Producto

def wishlist_view(request):
    """Vista de la lista de deseos"""
    # Debug: mostrar información del usuario
    print(f"=== DEBUG WISHLIST ===")
    print(f"Usuario logueado: {request.user.username} (ID: {request.user.id})")
    print(f"Está autenticado: {request.user.is_authenticated}")
    print(f"Tipo de usuario: {type(request.user)}")
    
    # Verificar si el usuario existe en la base de datos
    from django.contrib.auth.models import User
    try:
        db_user = User.objects.get(id=request.user.id)
        print(f"Usuario encontrado en DB: {db_user.username}")
    except User.DoesNotExist:
        print("ERROR: Usuario no encontrado en la base de datos")
        messages.error(request, "Error: Usuario no encontrado.")
        return redirect('account:login')
    
    # Si no está autenticado, mostrar mensaje pero no redirigir
    if not request.user.is_authenticated:
        print("Usuario no autenticado")
        messages.warning(request, "Debes iniciar sesión para ver tu lista de deseos.")
        context = {
            'page_title': 'Lista de Deseos',
            'wishlist_items': [],
            'debug_user': "No autenticado",
            'debug_count': 0,
            'debug_all_count': WishlistItem.objects.all().count()
        }
        return render(request, 'wishlist/wishlist.html', context)
    
    # Probar diferentes consultas para debug
    print(f"Usuario ID: {request.user.id}")
    print(f"Usuario username: {request.user.username}")
    
    # Consulta directa por ID de usuario
    wishlist_items_by_id = WishlistItem.objects.filter(usuario_id=request.user.id).select_related('producto')
    print(f"Elementos por ID de usuario: {wishlist_items_by_id.count()}")
    
    # Consulta por objeto usuario
    wishlist_items = WishlistItem.objects.filter(usuario=request.user).select_related('producto')
    print(f"Elementos por objeto usuario: {wishlist_items.count()}")
    
    # Consulta por username
    wishlist_items_by_username = WishlistItem.objects.filter(usuario__username=request.user.username).select_related('producto')
    print(f"Elementos por username: {wishlist_items_by_username.count()}")
    
    # Mostrar elementos encontrados
    for item in wishlist_items:
        print(f"  - {item.producto.nombre} (ID: {item.producto.id})")
    
    # Verificar si la consulta está funcionando
    all_wishlist_items = WishlistItem.objects.all()
    print(f"Total de elementos en wishlist: {all_wishlist_items.count()}")
    
    # Usar la consulta que funcione mejor
    wishlist_items = wishlist_items_by_id
    
    context = {
        'page_title': 'Lista de Deseos',
        'wishlist_items': wishlist_items,
        'debug_user': request.user.username if request.user.is_authenticated else "No autenticado",
        'debug_count': wishlist_items.count(),
        'debug_all_count': all_wishlist_items.count()
    }
    print("=== FIN DEBUG ===")
    return render(request, 'wishlist/wishlist.html', context)

@login_required
@require_POST
def add_to_wishlist(request, product_id):
    """Agregar producto a la lista de deseos"""
    try:
        producto = get_object_or_404(Producto, id=product_id)
        
        # Verificar si ya existe en el wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(
            usuario=request.user,
            producto=producto
        )
        
        if created:
            messages.success(request, f"'{producto.nombre}' agregado a tu lista de deseos.")
        else:
            messages.info(request, f"'{producto.nombre}' ya está en tu lista de deseos.")
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Producto agregado a la lista de deseos',
                'in_wishlist': True
            })
        
        return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist'))
        
    except Exception as e:
        messages.error(request, "Error al agregar el producto a la lista de deseos.")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Error al agregar el producto'
            })
        return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist'))

@login_required
@require_POST
def remove_from_wishlist(request, product_id):
    """Eliminar producto de la lista de deseos"""
    try:
        wishlist_item = get_object_or_404(WishlistItem, usuario=request.user, producto_id=product_id)
        producto_nombre = wishlist_item.producto.nombre
        wishlist_item.delete()
        
        messages.success(request, f"'{producto_nombre}' eliminado de tu lista de deseos.")
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Producto eliminado de la lista de deseos',
                'in_wishlist': False
            })
        
        return redirect('wishlist:wishlist')
        
    except Exception as e:
        messages.error(request, "Error al eliminar el producto de la lista de deseos.")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Error al eliminar el producto'
            })
        return redirect('wishlist:wishlist')

@login_required
def check_wishlist_status(request, product_id):
    """Verificar si un producto está en el wishlist del usuario"""
    try:
        in_wishlist = WishlistItem.objects.filter(
            usuario=request.user, 
            producto_id=product_id
        ).exists()
        
        return JsonResponse({
            'success': True,
            'in_wishlist': in_wishlist
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@require_POST
def clear_wishlist(request):
    """Limpiar toda la lista de deseos del usuario"""
    try:
        deleted_count = WishlistItem.objects.filter(usuario=request.user).delete()[0]
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Se eliminaron {deleted_count} productos de tu lista de deseos',
                'deleted_count': deleted_count
            })
        
        messages.success(request, f'Se eliminaron {deleted_count} productos de tu lista de deseos')
        return redirect('wishlist:wishlist')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Error al limpiar la lista de deseos'
            })
        
        messages.error(request, 'Error al limpiar la lista de deseos')
        return redirect('wishlist:wishlist')
