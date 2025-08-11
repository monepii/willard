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
    print(f"Autenticado: {request.user.is_authenticated}")
    
    # Si no está autenticado, mostrar mensaje de login
    if not request.user.is_authenticated:
        context = {
            'page_title': 'Lista de Deseos',
            'wishlist_items': [],
            'perfil': None,
        }
        return render(request, 'wishlist/wishlist.html', context)
    
    # Obtener wishlist del usuario
    items = WishlistItem.objects.filter(usuario=request.user).select_related('producto')
    items_count = items.count()
    print(f"Elementos encontrados para {request.user.username}: {items_count}")
    
    # Mostrar cada elemento
    for item in items:
        print(f"  - {item.producto.nombre} (ID: {item.producto.id})")
    
    # Obtener perfil del usuario
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        print(f"Perfil encontrado: {perfil.nombre}")
    except PerfilUsuario.DoesNotExist:
        print("No se encontró perfil, creando uno...")
        perfil = PerfilUsuario.objects.create(
            user=request.user,
            nombre=request.user.first_name or request.user.username,
            email=request.user.email,
            telefono='',
            direccion=''
        )
        print(f"Perfil creado: {perfil.nombre}")
    
    context = {
        'page_title': 'Lista de Deseos',
        'wishlist_items': items,
        'perfil': perfil,
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
