from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Carrito
from .models import Orden, ItemOrden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.urls import reverse
import os

try:
    import mercadopago
except Exception:
    mercadopago = None


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

    # Crear preferencia de Mercado Pago
    access_token = os.environ.get('MP_ACCESS_TOKEN') or getattr(settings, 'MP_ACCESS_TOKEN', None)
    public_key = os.environ.get('MP_PUBLIC_KEY') or getattr(settings, 'MP_PUBLIC_KEY', None)
    if not access_token:
        messages.error(request, 'Falta configurar MP_ACCESS_TOKEN en variables de entorno.')
        return redirect('checkout:checkout')

    sdk = mercadopago.SDK(access_token) if mercadopago else None
    if sdk is None:
        messages.error(request, 'SDK de Mercado Pago no disponible en el servidor.')
        return redirect('checkout:checkout')

    items_mp = []
    for item in orden.items.all():
        items_mp.append({
            "id": str(item.producto.id),
            "title": item.producto.nombre,
            "quantity": int(item.cantidad),
            "currency_id": "MXN",
            "unit_price": float(item.precio_unitario),
        })

    return_path = reverse('checkout:mp_return')
    success_url = request.build_absolute_uri(f"{return_path}?status=success&order_number={orden.numero_orden}")
    failure_url = request.build_absolute_uri(f"{return_path}?status=failure&order_number={orden.numero_orden}")
    pending_url = request.build_absolute_uri(f"{return_path}?status=pending&order_number={orden.numero_orden}")
    
    # Construir notification_url solo si no es localhost (Mercado Pago no puede acceder a localhost)
    notification_url = request.build_absolute_uri(reverse('checkout:mp_webhook'))
    # Solo incluir notification_url si es HTTPS y no es localhost
    include_notification = notification_url.startswith('https://') and 'localhost' not in notification_url and '127.0.0.1' not in notification_url

    preference_data = {
        "items": items_mp,
        "payer": {
            "name": nombre_completo,
            "email": email,
        },
        "back_urls": {
            "success": success_url,
            "failure": failure_url,
            "pending": pending_url,
        },
        "external_reference": str(orden.numero_orden),
        "statement_descriptor": "WILLARD",
    }
    
    # Solo agregar notification_url si es válida (HTTPS y no localhost)
    if include_notification:
        preference_data["notification_url"] = notification_url

    try:
        pref_response = sdk.preference().create(preference_data)
    except Exception as e:
        messages.error(request, f"Error al crear preferencia MP: {e}")
        return redirect('checkout:checkout')

    if not isinstance(pref_response, dict):
        messages.error(request, 'Respuesta inválida de Mercado Pago (sin diccionario).')
        return redirect('checkout:checkout')

    if 'response' not in pref_response:
        err_msg = pref_response.get('message') or pref_response.get('error') or 'Respuesta sin contenido.'
        messages.error(request, f"No se pudo crear la preferencia de pago: {err_msg}")
        return redirect('checkout:checkout')

    pref = pref_response.get("response", {})
    init_point = pref.get("init_point") or pref.get("sandbox_init_point")
    orden.mp_preference_id = pref.get("id")
    orden.mp_external_reference = str(orden.numero_orden)
    orden.save(update_fields=["mp_preference_id", "mp_external_reference"])

    # No limpiamos el carrito todavía; esperamos confirmación de pago
    if not init_point:
        messages.error(request, f"Preferencia creada sin URL de pago. Respuesta: {pref}")
        return redirect('checkout:checkout')
    messages.info(request, f"Redirigiendo a Mercado Pago...")
    return redirect(init_point)


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


@login_required
def mp_return(request):
    """Retorno de Mercado Pago (success/failure/pending)"""
    status = request.GET.get('status') or request.GET.get('collection_status')
    payment_id = request.GET.get('payment_id') or request.GET.get('collection_id')
    order_number = request.GET.get('order_number') or request.GET.get('external_reference')

    if not order_number:
        messages.error(request, 'Referencia de orden no encontrada.')
        return redirect('checkout:checkout')

    try:
        orden = Orden.objects.get(numero_orden=order_number, usuario=request.user)
    except Orden.DoesNotExist:
        messages.error(request, 'Orden no encontrada.')
        return redirect('checkout:checkout')

    if payment_id:
        orden.mp_payment_id = str(payment_id)
    if status:
        orden.mp_status = status

    # Si aprobado, marcamos como procesando y limpiamos carrito
    if status in ('approved', 'success'):
        orden.estado = 'procesando'
        try:
            carrito = Carrito.obtener_o_crear_carrito(request)
            carrito.limpiar()
        except Exception:
            pass

    orden.save()
    messages.info(request, f"Mercado Pago retorno: status={status}, payment_id={payment_id}")
    return redirect('checkout:success', order_number=orden.numero_orden)


@csrf_exempt
@require_POST
def mp_webhook(request):
    """Webhook de Mercado Pago para notificaciones de pago"""
    try:
        data = request.body.decode('utf-8')
    except Exception:
        data = ''

    try:
        import json
        payload = json.loads(data) if data else {}
    except Exception:
        payload = {}

    topic = request.GET.get('type') or request.GET.get('topic') or payload.get('type')
    payment_id = request.GET.get('data.id') or (payload.get('data', {}) or {}).get('id')

    access_token = os.environ.get('MP_ACCESS_TOKEN')
    if mercadopago and access_token and topic in ('payment', 'payments') and payment_id:
        sdk = mercadopago.SDK(access_token)
        try:
            payment_info = sdk.payment().get(payment_id)
            info = payment_info.get('response', {})
            status = info.get('status')
            external_reference = info.get('external_reference')
            if external_reference:
                try:
                    orden = Orden.objects.get(numero_orden=external_reference)
                    orden.mp_payment_id = str(payment_id)
                    orden.mp_status = status
                    if status == 'approved':
                        orden.estado = 'procesando'
                    elif status in ('rejected', 'cancelled', 'canceled'):
                        orden.estado = 'cancelado'
                    orden.save()
                except Orden.DoesNotExist:
                    pass
        except Exception:
            pass

    return HttpResponse(status=200)
