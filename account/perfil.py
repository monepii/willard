from .models import PerfilUsuario

def perfil_usuario(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
        except PerfilUsuario.DoesNotExist:
            perfil = None
    else:
        perfil = None
    return {'perfil': perfil}