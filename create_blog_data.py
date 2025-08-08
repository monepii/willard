#!/usr/bin/env python
"""
Script para crear datos de prueba para el blog
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.models import Blog

def create_blog_data():
    """Crear datos de prueba para el blog"""
    
    # Crear posts del blog
    blog_posts = [
        {
            'titulo': 'How to Seal Damaged Dry-Wall',
            'contenido': '''Repairing damaged drywall is a common DIY task that can save you money and improve your home's appearance. In this comprehensive guide, we'll walk you through the process of sealing and repairing damaged drywall.

First, assess the damage:
- Small holes (nail holes, screws)
- Medium holes (doorknob damage)
- Large holes (furniture damage)
- Cracks and seams

Materials you'll need:
- Drywall compound
- Drywall tape
- Sandpaper (various grits)
- Putty knife
- Primer and paint

Step-by-step process:
1. Clean the damaged area
2. Apply drywall tape if needed
3. Apply joint compound
4. Sand the surface
5. Prime and paint

With the right tools and techniques, you can achieve professional-looking results.''',
            'autor': 'Equipo Willard',
            'publicado': True
        },
        {
            'titulo': 'Replacing the Doorbell Yourself Tips',
            'contenido': '''Replacing a doorbell is a simple DIY project that can be completed in under an hour. Whether you're upgrading to a wireless system or fixing a broken doorbell, this guide will help you do it safely and correctly.

Tools needed:
- Screwdriver
- Wire strippers
- Voltage tester
- Drill (if mounting new location)

Safety first:
- Turn off power to the doorbell circuit
- Test wires with voltage tester
- Wear safety glasses when drilling

Installation steps:
1. Remove old doorbell
2. Disconnect wires
3. Mount new doorbell
4. Connect wires
5. Test the system

Modern doorbells offer features like:
- Video cameras
- Motion detection
- Smartphone notifications
- Two-way communication

Choose the right doorbell for your needs and budget.''',
            'autor': 'Carlos Martínez',
            'publicado': True
        },
        {
            'titulo': 'Garden Supplies Buying Guide',
            'contenido': '''Creating a beautiful garden requires the right tools and supplies. This comprehensive buying guide will help you choose the best garden supplies for your needs, whether you're a beginner or experienced gardener.

Essential garden tools:
- Shovels and spades
- Rakes and hoes
- Pruning shears
- Watering cans and hoses
- Garden gloves

Soil and fertilizers:
- Potting soil
- Compost
- Organic fertilizers
- pH testing kits

Plant care supplies:
- Plant markers
- Trellises and supports
- Pest control products
- Mulch and ground cover

Seasonal considerations:
- Spring: Seeds, soil, and tools
- Summer: Watering systems, pest control
- Fall: Bulbs, mulch, and cleanup tools
- Winter: Protection and storage

Invest in quality tools that will last for years.''',
            'autor': 'María González',
            'publicado': True
        },
        {
            'titulo': 'Guide to Buying the Tile Saw',
            'contenido': '''A tile saw is an essential tool for any tile installation project. Whether you're tiling a bathroom, kitchen, or outdoor space, choosing the right tile saw will make your job easier and produce better results.

Types of tile saws:
- Wet saws (most common)
- Dry saws (for quick cuts)
- Handheld tile cutters
- Bridge saws (for large tiles)

Key features to consider:
- Blade size and type
- Water reservoir capacity
- Cutting depth and width
- Portability and storage
- Safety features

Popular brands and models:
- Professional grade saws
- DIY-friendly options
- Budget considerations
- Rental vs. purchase

Maintenance and care:
- Blade replacement
- Water system cleaning
- Storage recommendations
- Safety precautions

Make an informed decision based on your project needs.''',
            'autor': 'Equipo Willard',
            'publicado': True
        }
    ]
    
    for post_data in blog_posts:
        post, created = Blog.objects.get_or_create(
            titulo=post_data['titulo'],
            defaults={
                'contenido': post_data['contenido'],
                'autor': post_data['autor'],
                'publicado': post_data['publicado']
            }
        )
        
        if created:
            print(f"Post del blog creado: {post.titulo}")
        else:
            print(f"Post del blog ya existe: {post.titulo}")

if __name__ == '__main__':
    print("Creando datos de prueba para el blog...")
    create_blog_data()
    print("¡Datos de prueba del blog creados exitosamente!")
