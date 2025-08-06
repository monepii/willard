from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import WishlistItem
from ferretetia.models import Producto
from account.models import PerfilUsuario

def wishlist_view(request):
    """Vista de la lista de deseos"""
    print("=== WISHLIST DEBUG ===")
    print(f"Usuario: {request.user.username}")
    print(f"ID: {request.user.id}")
    print(f"Autenticado: {request.user.is_authenticated}")
    print(f"Tipo de usuario: {type(request.user)}")
    print(f"Es anónimo: {request.user.is_anonymous}")
    
    # Verificar sesión
    if hasattr(request, 'session'):
        print(f"Session ID: {request.session.session_key}")
        if '_auth_user_id' in request.session:
            print(f"Auth user ID en sesión: {request.session['_auth_user_id']}")
        else:
            print("No hay auth_user_id en sesión")
    
    # Si no está autenticado, mostrar mensaje de login
    if not request.user.is_authenticated:
        context = {
            'page_title': 'Lista de Deseos',
            'wishlist_items': [],
            'perfil': None,
            'debug_user': "No autenticado",
            'debug_count': 0,
            'debug_all_count': 0
        }
        return render(request, 'wishlist/wishlist.html', context)
    
    # Obtener wishlist del usuario con productos relacionados y convertir a lista
    items = list(WishlistItem.objects.filter(usuario=request.user).select_related('producto'))
    print(f"Elementos encontrados: {items.count()}")
    print(f"Usuario actual: {request.user.username} (ID: {request.user.id})")
    print(f"Usuario autenticado: {request.user.is_authenticated}")
    
    # Mostrar cada elemento
    for item in items:
        print(f"  - {item.producto.nombre}")
    
    # Verificar si hay items en total
    all_items = WishlistItem.objects.all()
    print(f"Total de items en wishlist (todos los usuarios): {all_items.count()}")
    for item in all_items:
        print(f"  - {item.usuario.username} -> {item.producto.nombre}")
    
    # Obtener o crear perfil del usuario
    perfil, created = PerfilUsuario.objects.get_or_create(
        user=request.user,
        defaults={
            'nombre': request.user.first_name or request.user.username,
            'email': request.user.email,
            'telefono': '',
            'direccion': ''
        }
    )
    
    context = {
        'page_title': 'Lista de Deseos',
        'wishlist_items': items,
        'perfil': perfil,  # Usar el perfil del modelo PerfilUsuario
        'debug_user': request.user.username,
        'debug_count': items.count(),
        'debug_all_count': WishlistItem.objects.all().count()
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
