from django.contrib.auth import get_user_model
from wishlist.models import WishlistItem
from ferretetia.models import Producto

# Cambia el username por el tuyo
user = get_user_model().objects.get(username='TU_USUARIO')

# Cambia el id por el de un producto existente
producto = Producto.objects.first()

WishlistItem.objects.get_or_create(usuario=user, producto=producto)
print('Producto agregado a la wishlist de', user.username)
