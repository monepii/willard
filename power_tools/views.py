from django.shortcuts import render
from django.http import Http404

def power_tools_view(request):
    """Vista principal de herramientas eléctricas"""
    products = [
        {'id': 1, 'name': 'Taladro Inalámbrico', 'price': 89.99, 'category': 'drill'},
        {'id': 2, 'name': 'Sierra Circular', 'price': 129.99, 'category': 'saw'},
        {'id': 3, 'name': 'Lijadora Orbital', 'price': 65.99, 'category': 'sander'},
        {'id': 4, 'name': 'Amoladora Angular', 'price': 75.50, 'category': 'grinder'},
        {'id': 5, 'name': 'Fresadora', 'price': 150.00, 'category': 'router'},
        {'id': 6, 'name': 'Martillo Perforador', 'price': 120.99, 'category': 'hammer'}
    ]
    
    context = {
        'page_title': 'Herramientas Eléctricas',
        'products': products
    }
    return render(request, 'power_tools/power_tools.html', context)

def power_tools_category(request, category):
    """Vista de herramientas por categoría"""
    all_products = [
        {'id': 1, 'name': 'Taladro Inalámbrico', 'price': 89.99, 'category': 'drill'},
        {'id': 2, 'name': 'Sierra Circular', 'price': 129.99, 'category': 'saw'},
        {'id': 3, 'name': 'Lijadora Orbital', 'price': 65.99, 'category': 'sander'},
        {'id': 4, 'name': 'Amoladora Angular', 'price': 75.50, 'category': 'grinder'},
        {'id': 5, 'name': 'Fresadora', 'price': 150.00, 'category': 'router'},
        {'id': 6, 'name': 'Martillo Perforador', 'price': 120.99, 'category': 'hammer'}
    ]
    
    filtered_products = [p for p in all_products if p['category'] == category]
    
    category_names = {
        'drill': 'Taladros',
        'saw': 'Sierras',
        'sander': 'Lijadoras',
        'grinder': 'Amoladoras',
        'router': 'Fresadoras',
        'hammer': 'Martillos'
    }
    
    context = {
        'page_title': f'Herramientas Eléctricas - {category_names.get(category, category.title())}',
        'products': filtered_products,
        'category': category,
        'category_name': category_names.get(category, category.title())
    }
    return render(request, 'power_tools/power_tools.html', context)

def product_detail(request, product_id):
    """Vista de detalle de un producto"""
    products = {
        1: {'id': 1, 'name': 'Taladro Inalámbrico', 'price': 89.99, 'category': 'drill', 'description': 'Taladro inalámbrico de alta potencia...'},
        2: {'id': 2, 'name': 'Sierra Circular', 'price': 129.99, 'category': 'saw', 'description': 'Sierra circular profesional...'},
        3: {'id': 3, 'name': 'Lijadora Orbital', 'price': 65.99, 'category': 'sander', 'description': 'Lijadora orbital para acabados perfectos...'}
    }
    
    if product_id not in products:
        raise Http404("Producto no encontrado")
    
    context = {
        'page_title': products[product_id]['name'],
        'product': products[product_id]
    }
    return render(request, 'power_tools/product_detail.html', context)
