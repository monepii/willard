from django.urls import path
from . import views

app_name = 'ferretetia'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    path('ferreteria/', views.index, name='ferreteria'),
    
    # Shop y elementos que permanecen en ferretetia
    path('shop/', views.shop, name='shop'),
    path('elements/', views.elements, name='elements'),
    
    # API
    path('api/search/', views.search_products, name='search_products'),
    
]
