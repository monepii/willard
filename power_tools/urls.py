from django.urls import path
from . import views

app_name = 'power_tools'

urlpatterns = [
    path('', views.power_tools_view, name='power_tools'),
    path('category/<str:category>/', views.power_tools_category, name='category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
