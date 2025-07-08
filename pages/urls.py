from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.pages_view, name='pages'),
    path('<str:page_name>/', views.page_detail, name='page_detail'),
]
