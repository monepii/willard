from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog'),
    path('post/<int:post_id>/', views.blog_detail, name='post_detail'),
    path('category/<str:category>/', views.blog_category, name='category'),
]
