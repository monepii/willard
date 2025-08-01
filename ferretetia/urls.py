from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static   

app_name = 'ferretetia'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    path('ferreteria/', views.index, name='ferreteria'),
    
    # Shop y elementos que permanecen en ferretetia
    path('shop/', views.shop, name='shop'),
    path('elements/', views.elements, name='elements'),
    path('account/', views.account,name='account'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('compare/', views.compare, name='compare'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


