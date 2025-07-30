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

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


