from django.core.management.base import BaseCommand
from ferretetia.models import Producto, Categoria, Subcategoria


class Command(BaseCommand):
    help = 'Asigna subcategorías a los productos existentes basándose en su categoría'

    def handle(self, *args, **kwargs):
        productos_actualizados = 0
        productos_sin_categoria = 0
        productos_sin_subcategoria = 0
        
        # Mapeo de categorías a subcategorías por defecto (primera subcategoría de cada categoría)
        subcategorias_por_categoria = {}
        
        # Obtener la primera subcategoría de cada categoría
        for categoria in Categoria.objects.all():
            primera_subcat = categoria.subcategorias.filter(activa=True).first()
            if primera_subcat:
                subcategorias_por_categoria[categoria.id] = primera_subcat
        
        # Obtener productos sin subcategoría
        productos = Producto.objects.filter(subcategoria__isnull=True)
        
        self.stdout.write(f"Encontrados {productos.count()} productos sin subcategoría")
        
        for producto in productos:
            if not producto.categoria:
                productos_sin_categoria += 1
                self.stdout.write(
                    self.style.WARNING(f"⚠ Producto '{producto.nombre}' no tiene categoría asignada")
                )
                continue
            
            # Buscar subcategoría por defecto para esta categoría
            subcategoria_default = subcategorias_por_categoria.get(producto.categoria.id)
            
            if subcategoria_default:
                producto.subcategoria = subcategoria_default
                producto.save()
                productos_actualizados += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ '{producto.nombre}' → {producto.categoria.nombre} - {subcategoria_default.nombre}"
                    )
                )
            else:
                productos_sin_subcategoria += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠ No hay subcategorías para la categoría '{producto.categoria.nombre}'"
                    )
                )
        
        # Resumen
        self.stdout.write(self.style.SUCCESS(f'\n===== RESUMEN ====='))
        self.stdout.write(self.style.SUCCESS(f'Productos actualizados: {productos_actualizados}'))
        if productos_sin_categoria > 0:
            self.stdout.write(self.style.WARNING(f'Productos sin categoría: {productos_sin_categoria}'))
        if productos_sin_subcategoria > 0:
            self.stdout.write(self.style.WARNING(f'Productos sin subcategorías disponibles: {productos_sin_subcategoria}'))
        
        # Mostrar estadísticas por subcategoría
        self.stdout.write(self.style.SUCCESS(f'\n===== DISTRIBUCIÓN ====='))
        for categoria in Categoria.objects.all():
            self.stdout.write(f'\n{categoria.nombre}:')
            for subcategoria in categoria.subcategorias.all():
                count = subcategoria.productos.count()
                self.stdout.write(f'  - {subcategoria.nombre}: {count} productos')
