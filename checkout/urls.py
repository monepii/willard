from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('process/', views.process_order, name='process'),
    path('success/<str:order_number>/', views.checkout_success, name='success'),
]
