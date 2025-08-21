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
    
]
