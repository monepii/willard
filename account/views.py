from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from .forms import PerfilForm, DireccionForm
from .models import PerfilUsuario, Direccion
from checkout.models import Orden


def account_view(request):
    """Vista principal de la cuenta"""
    perfil = None
    direcciones = []
    ordenes_recientes = []
    
    if request.user.is_authenticated:
        try:
            from .models import PerfilUsuario
            perfil = PerfilUsuario.objects.get(user=request.user)
            direcciones = Direccion.objects.filter(user=request.user, activa=True)
            # Obtener las 3 órdenes más recientes
            ordenes_recientes = Orden.objects.filter(usuario=request.user).order_by('-creado')[:3]
        except PerfilUsuario.DoesNotExist:
            perfil = None
    
    context = {
        'page_title': 'Mi Cuenta',
        'user': request.user if request.user.is_authenticated else None,
        'perfil': perfil,
        'direcciones': direcciones,
        'ordenes_recientes': ordenes_recientes
    }
    return render(request, 'account/account.html', context)

def login_view(request):
    """Vista de login"""
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account:account')
        else:
            messages.error(request, 'Credenciales incorrectas')
    context = {
        'page_title': 'Iniciar Sesión',
        'form': form
    }
    return render(request, 'account/login.html', context)
from .forms import RegistroUsuarioForm, PerfilForm

def register_view(request):
    """Vista de registro"""
    if request.method == 'POST':
        user_form = RegistroUsuarioForm(request.POST)
        perfil_form = PerfilForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.email = user.email
            perfil.save()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente')
            return redirect('account:account')
        else:
            messages.error(request, 'Corrige los errores en el formulario')
    else:
        user_form = RegistroUsuarioForm()
        perfil_form = PerfilForm()
    context = {
        'page_title': 'Crear Cuenta',
        'form': user_form,
        'perfil_form': perfil_form
    }
    return render(request, 'account/register.html', context)

@login_required
def profile_view(request):
    """Vista del perfil del usuario"""
    context = {
        'page_title': 'Mi Perfil',
        'user': request.user
    }
    return render(request, 'account/profile.html', context)

def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('ferretetia:index')


@login_required
def update_view(request):
    try:
        perfil = request.user.perfilusuario 
    except PerfilUsuario.DoesNotExist:
        messages.error(request, "Tu perfil no existe.")
        return redirect('account:account')

    if request.method == "POST":
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
    else:
        form = PerfilForm(instance=perfil)  

    return render(request, "account/update.html", {"form": form})

# Vistas para gestión de direcciones
@login_required
def direcciones_view(request):
    """Vista para listar todas las direcciones del usuario"""
    direcciones = Direccion.objects.filter(user=request.user, activa=True)
    context = {
        'page_title': 'Mis Direcciones',
        'direcciones': direcciones
    }
    return render(request, 'account/direcciones.html', context)

@login_required
def agregar_direccion_view(request):
    """Vista para agregar una nueva dirección"""
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.user = request.user
            direccion.save()
            messages.success(request, 'Dirección agregada exitosamente.')
            return redirect('account:direcciones')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = DireccionForm()
    
    context = {
        'page_title': 'Agregar Dirección',
        'form': form
    }
    return render(request, 'account/agregar_direccion.html', context)

@login_required
def editar_direccion_view(request, direccion_id):
    """Vista para editar una dirección existente"""
    direccion = get_object_or_404(Direccion, id=direccion_id, user=request.user)
    
    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dirección actualizada exitosamente.')
            return redirect('account:direcciones')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = DireccionForm(instance=direccion)
    
    context = {
        'page_title': 'Editar Dirección',
        'form': form,
        'direccion': direccion
    }
    return render(request, 'account/editar_direccion.html', context)

@login_required
def eliminar_direccion_view(request, direccion_id):
    """Vista para eliminar una dirección (soft delete)"""
    direccion = get_object_or_404(Direccion, id=direccion_id, user=request.user)
    
    if request.method == 'POST':
        direccion.activa = False
        direccion.save()
        messages.success(request, 'Dirección eliminada exitosamente.')
        return redirect('account:direcciones')
    
    context = {
        'page_title': 'Eliminar Dirección',
        'direccion': direccion
    }
    return render(request, 'account/eliminar_direccion.html', context)

@login_required
def establecer_principal_view(request, direccion_id):
    """Vista para establecer una dirección como principal"""
    direccion = get_object_or_404(Direccion, id=direccion_id, user=request.user)
    
    if request.method == 'POST':
        # Desmarcar todas las direcciones principales del usuario
        Direccion.objects.filter(user=request.user, es_principal=True).update(es_principal=False)
        # Marcar esta dirección como principal
        direccion.es_principal = True
        direccion.save()
        messages.success(request, 'Dirección principal actualizada.')
    
    return redirect('account:direcciones')


@login_required
def historial_pedidos_view(request):
    """Vista para mostrar el historial completo de pedidos del usuario"""
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-creado')
    
    context = {
        'page_title': 'Historial de Pedidos',
        'ordenes': ordenes
    }
    return render(request, 'account/historial_pedidos.html', context)


@login_required
def detalle_pedido_view(request, numero_orden):
    """Vista para mostrar el detalle de un pedido específico"""
    orden = get_object_or_404(Orden, numero_orden=numero_orden, usuario=request.user)
    
    context = {
        'page_title': f'Pedido #{orden.numero_orden}',
        'orden': orden
    }
    return render(request, 'account/detalle_pedido.html', context)
