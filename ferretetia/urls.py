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
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('search/', views.search_products, name='search_products'),
    path('test-search/', views.test_search, name='test_search'),
    path('elements/', views.elements, name='elements'),
    # path('account/', views.account,name='account'),  # COMENTADO - MANEJADO POR account.urls
    # path('wishlist/', views.wishlist, name='wishlist'),  # COMENTADO - MANEJADO POR wishlist.urls
    # path('compare/', views.compare, name='compare'),  # COMENTADO - MANEJADO POR compare.urls
    # path('checkout/', views.checkout, name='checkout'),  # COMENTADO - MANEJADO POR checkout.urls
    path('blog /', views.blog, name='blog'),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    