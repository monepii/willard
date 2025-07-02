from django.urls import path
from . import views

app_name = 'ferretetia'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    path('ferreteria/', views.index, name='ferreteria'),
    
    # Navegación superior
    path('wishlist/', views.wishlist, name='wishlist'),
    path('compare/', views.compare, name='compare'),
    path('account/', views.account, name='account'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    
    # Navegación del menú inferior
    path('power-tools/', views.power_tools, name='power_tools'),
    path('blog/', views.blog, name='blog'),
    path('shop/', views.shop, name='shop'),
    path('pages/', views.pages, name='pages'),
    path('elements/', views.elements, name='elements'),
    
    # API
    path('api/search/', views.search_products, name='search_products'),
]
