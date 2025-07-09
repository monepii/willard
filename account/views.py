from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:account')
        else:
            messages.error(request, 'Credenciales incorrectas')
    
    context = {'page_title': 'Iniciar Sesión'}
    return render(request, 'account/login.html', context)

def register_view(request):
    """Vista de registro"""
    from .forms import RegistroUsuarioForm, PerfilUsuarioForm
    if request.method == 'POST':
        user_form = RegistroUsuarioForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)
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
        user_form = RegistroUsuarioForm()
        perfil_form = PerfilUsuarioForm()
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
