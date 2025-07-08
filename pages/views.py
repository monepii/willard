from django.shortcuts import render
from django.http import Http404

def pages_view(request):
    """Vista principal de páginas"""
    context = {
        'page_title': 'Páginas',
        'available_pages': [
            {'name': 'about', 'title': 'Acerca de Nosotros'},
            {'name': 'contact', 'title': 'Contacto'},
            {'name': 'services', 'title': 'Servicios'},
            {'name': 'delivery', 'title': 'Entregas'},
            {'name': 'warranty', 'title': 'Garantías'},
            {'name': 'faq', 'title': 'Preguntas Frecuentes'}
        ]
    }
    return render(request, 'pages/pages.html', context)

def page_detail(request, page_name):
    """Vista de detalle de una página específica"""
    pages_content = {
        'about': {
            'title': 'Acerca de Nosotros',
            'content': 'WILLARD es una ferretería con más de 20 años de experiencia...'
        },
        'contact': {
            'title': 'Contacto',
            'content': 'Ponte en contacto con nosotros...'
        },
        'services': {
            'title': 'Servicios',
            'content': 'Ofrecemos una amplia gama de servicios...'
        },
        'delivery': {
            'title': 'Entregas',
            'content': 'Información sobre nuestro servicio de entrega...'
        },
        'warranty': {
            'title': 'Garantías',
            'content': 'Todos nuestros productos incluyen garantía...'
        },
        'faq': {
            'title': 'Preguntas Frecuentes',
            'content': 'Aquí encontrarás respuestas a las preguntas más comunes...'
        }
    }
    
    if page_name not in pages_content:
        raise Http404("Página no encontrada")
    
    context = {
        'page_title': pages_content[page_name]['title'],
        'page_content': pages_content[page_name]['content'],
        'page_name': page_name
    }
    return render(request, 'pages/page_detail.html', context)
