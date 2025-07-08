from django.shortcuts import render, get_object_or_404
from django.http import Http404

def blog_list(request):
    """Vista del listado de posts del blog"""
    # Datos de ejemplo
    posts = [
        {
            'id': 1,
            'title': 'Cómo elegir el martillo correcto',
            'excerpt': 'Guía completa para seleccionar el martillo ideal según el trabajo.',
            'date': '2025-07-01',
            'category': 'tips'
        },
        {
            'id': 2,
            'title': 'Mantenimiento de herramientas eléctricas',
            'excerpt': 'Consejos esenciales para mantener tus herramientas en perfecto estado.',
            'date': '2025-06-28',
            'category': 'maintenance'
        },
        {
            'id': 3,
            'title': 'Seguridad en el taller',
            'excerpt': 'Normas básicas de seguridad que todo trabajador debe conocer.',
            'date': '2025-06-25',
            'category': 'safety'
        }
    ]
    
    context = {
        'page_title': 'Blog de Ferretería',
        'posts': posts
    }
    return render(request, 'blog/blog.html', context)

def blog_detail(request, post_id):
    """Vista de detalle de un post"""
    # Simulamos obtener un post específico
    posts = {
        1: {
            'id': 1,
            'title': 'Cómo elegir el martillo correcto',
            'content': 'Contenido completo del artículo sobre martillos...',
            'date': '2025-07-01',
            'category': 'tips'
        },
        2: {
            'id': 2,
            'title': 'Mantenimiento de herramientas eléctricas',
            'content': 'Contenido completo sobre mantenimiento...',
            'date': '2025-06-28',
            'category': 'maintenance'
        }
    }
    
    if post_id not in posts:
        raise Http404("Post no encontrado")
    
    context = {
        'page_title': posts[post_id]['title'],
        'post': posts[post_id]
    }
    return render(request, 'blog/post_detail.html', context)

def blog_category(request, category):
    """Vista de posts por categoría"""
    # Filtrar posts por categoría
    all_posts = [
        {'id': 1, 'title': 'Cómo elegir el martillo correcto', 'category': 'tips', 'date': '2025-07-01'},
        {'id': 2, 'title': 'Mantenimiento de herramientas eléctricas', 'category': 'maintenance', 'date': '2025-06-28'},
        {'id': 3, 'title': 'Seguridad en el taller', 'category': 'safety', 'date': '2025-06-25'},
        {'id': 4, 'title': 'Review: Taladro XYZ', 'category': 'reviews', 'date': '2025-06-20'},
        {'id': 5, 'title': 'Tutorial: Uso básico de la sierra', 'category': 'tutorials', 'date': '2025-06-15'}
    ]
    
    filtered_posts = [post for post in all_posts if post['category'] == category]
    
    category_names = {
        'tips': 'Consejos y Trucos',
        'maintenance': 'Mantenimiento',
        'safety': 'Seguridad',
        'reviews': 'Reseñas de Productos',
        'tutorials': 'Tutoriales'
    }
    
    context = {
        'page_title': f'Blog - {category_names.get(category, category.title())}',
        'posts': filtered_posts,
        'category': category,
        'category_name': category_names.get(category, category.title())
    }
    return render(request, 'blog/blog.html', context)
