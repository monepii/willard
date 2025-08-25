from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import PerfilForm
from .models import PerfilUsuario


def account_view(request):
    """Vista principal de la cuenta"""
    perfil = None
    if request.user.is_authenticated:
        try:
            from .models import PerfilUsuario
            perfil = PerfilUsuario.objects.get(user=request.user)
        except PerfilUsuario.DoesNotExist:
            perfil = None
    context = {
        'page_title': 'Mi Cuenta',
        'user': request.user if request.user.is_authenticated else None,
        'perfil': perfil
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
