from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Carrito
from .models import Orden, ItemOrden
from django.views.decorators.http import require_POST
from decimal import Decimal


@login_required
def checkout_view(request):
    """Vista de checkout/finalizar compra"""
    from account.models import Direccion, PerfilUsuario
    
    carrito = Carrito.obtener_o_crear_carrito(request)
    if not carrito or carrito.total_items == 0:
        messages.info(request, "Tu carrito está vacío.")
        return redirect('cart:cart')

    # Verificar que el usuario tenga al menos una dirección
    direcciones = Direccion.objects.filter(user=request.user, activa=True).order_by('-es_principal', '-creada')
    if not direcciones.exists():
        messages.warning(request, "Necesitas agregar al menos una dirección para continuar con tu pedido.")
        return redirect('account:agregar_direccion')

    items = carrito.items.all()
    subtotal = carrito.total_precio
    impuestos = Decimal('0.00')
    envio = Decimal('0.00')
    total = subtotal + impuestos + envio
    
    direccion_principal = direcciones.filter(es_principal=True).first()
    
    # Obtener perfil del usuario para prellenar datos
    perfil = None
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        pass

    context = {
        'page_title': 'Finalizar Compra',
        'carrito': carrito,
        'items': items,
        'subtotal': subtotal,
        'impuestos': impuestos,
        'envio': envio,
        'total': total,
        'direcciones': direcciones,
        'direccion_principal': direccion_principal,
        'perfil': perfil,
    }
    return render(request, 'checkout/checkout.html', context)


@login_required
@require_POST
def process_order(request):
    """Procesa el formulario de checkout y crea la orden"""
    from account.models import Direccion
    
    carrito = Carrito.obtener_o_crear_carrito(request)
    if not carrito or carrito.total_items == 0:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('cart:cart')

    direccion_id = request.POST.get('direccion_existente')
    
    if not direccion_id:
        messages.error(request, "Debe seleccionar una dirección de envío.")
        return redirect('checkout:checkout')
    
    # Usar dirección existente
    try:
        direccion_obj = Direccion.objects.get(id=direccion_id, user=request.user, activa=True)
        # Construir datos desde la dirección existente
        nombre_completo = request.POST.get('nombre_completo') or f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        email = request.POST.get('email') or request.user.email
        direccion_completa = f"{direccion_obj.calle} #{direccion_obj.numero_exterior}"
        if direccion_obj.numero_interior:
            direccion_completa += f" Int. {direccion_obj.numero_interior}"
        direccion_completa += f", {direccion_obj.colonia}"
        ciudad = f"{direccion_obj.municipio}, {direccion_obj.estado}"
        codigo_postal = direccion_obj.codigo_postal
        telefono = direccion_obj.telefono or request.POST.get('telefono', '')
    except Direccion.DoesNotExist:
        messages.error(request, "Dirección seleccionada no encontrada.")
        return redirect('checkout:checkout')

    notas = request.POST.get('notas', '')

    # Validar campos requeridos
    if not all([nombre_completo, email, direccion_completa, ciudad, codigo_postal]):
        messages.error(request, "Por favor completa todos los campos requeridos.")
        return redirect('checkout:checkout')

    subtotal = carrito.total_precio
    impuestos = Decimal('0.00')
    envio = Decimal('0.00')
    total = subtotal + impuestos + envio

    orden = Orden.objects.create(
        usuario=request.user,
        nombre_completo=nombre_completo,
        email=email,
        direccion=direccion_completa,
        ciudad=ciudad,
        codigo_postal=codigo_postal,
        telefono=telefono,
        subtotal=subtotal,
        impuestos=impuestos,
        envio=envio,
        total=total,
        notas=notas,
    )

    for item in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            precio_total=item.precio_total,
        )

    # Vaciar carrito tras crear la orden
    carrito.limpiar()

    messages.success(request, "¡Tu orden ha sido creada exitosamente!")
    return redirect('checkout:success', order_number=orden.numero_orden)


@login_required
def checkout_success(request, order_number=None):
    """Vista de confirmación de compra exitosa"""
    numero = order_number or request.GET.get('order_number')
    orden = None
    if numero:
        try:
            orden = Orden.objects.get(numero_orden=numero, usuario=request.user)
        except Orden.DoesNotExist:
            orden = None

    context = {
        'page_title': 'Compra Exitosa',
        'order_number': numero,
        'orden': orden,
    }
    return render(request, 'checkout/success.html', context)
