from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Blog

def blog_list(request):
    """Vista del listado de posts del blog"""
    posts = Blog.objects.filter(publicado=True).order_by('-fecha')
    
    context = {
        'page_title': 'Blog de Ferretería',
        'posts': posts
    }
    return render(request, 'blog/blog.html', context)

def blog_detail(request, post_id):
    """Vista de detalle de un post"""
    post = get_object_or_404(Blog, id=post_id, publicado=True)
    
    context = {
        'page_title': post.titulo,
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)

def blog_category(request, category):
    """Vista de posts por categoría"""
    # Por ahora usamos el campo autor como categoría, pero puedes agregar un campo categoría al modelo
    posts = Blog.objects.filter(publicado=True, autor__icontains=category).order_by('-fecha')
    
    context = {
        'page_title': f'Blog - {category.title()}',
        'posts': posts,
        'category': category,
        'category_name': category.title()
    }
    return render(request, 'blog/blog.html', context)
