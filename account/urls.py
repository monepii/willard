from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account_view, name='account'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('update/', views.update_view, name="update"),
    
    # URLs para gestión de direcciones
    path('direcciones/', views.direcciones_view, name='direcciones'),
    path('direcciones/agregar/', views.agregar_direccion_view, name='agregar_direccion'),
    path('direcciones/editar/<int:direccion_id>/', views.editar_direccion_view, name='editar_direccion'),
    path('direcciones/eliminar/<int:direccion_id>/', views.eliminar_direccion_view, name='eliminar_direccion'),
    path('direcciones/principal/<int:direccion_id>/', views.establecer_principal_view, name='establecer_principal'),
    
    # URLs para historial de pedidos
    path('pedidos/', views.historial_pedidos_view, name='historial_pedidos'),
    path('pedidos/<str:numero_orden>/', views.detalle_pedido_view, name='detalle_pedido'),
]
