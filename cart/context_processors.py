from .utils import get_cart_summary


def cart_context(request):
    """Context processor para hacer el carrito disponible globalmente"""
    try:
        if request.user.is_authenticated:
            cart_summary = get_cart_summary(request)
            return {
                'cart_count': cart_summary['total_items'],
                'cart_total': cart_summary['total_precio'],
                'cart_is_empty': cart_summary['is_empty']
            }
        else:
            # Para usuarios no autenticados, mostrar valores por defecto
            return {
                'cart_count': 0,
                'cart_total': 0,
                'cart_is_empty': True
            }
    except Exception:
        # Si hay algún error, retornar valores por defecto
        return {
            'cart_count': 0,
            'cart_total': 0,
            'cart_is_empty': True
        } 