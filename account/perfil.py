from .models import PerfilUsuario

def perfil_usuario(request):
    if request.user.is_authenticated:
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
        except PerfilUsuario.DoesNotExist:
            perfil = None
    else:
        perfil = None
    return {'perfil': perfil}