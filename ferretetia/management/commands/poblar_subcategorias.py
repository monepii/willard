from django.core.management.base import BaseCommand
from ferretetia.models import Categoria, Subcategoria


class Command(BaseCommand):
    help = 'Pobla la base de datos con subcategorías para cada categoría existente'

    def handle(self, *args, **kwargs):
        # Definir subcategorías por categoría
        subcategorias_data = {
            'Herramientas': [
                {'nombre': 'Herramientas Manuales', 'descripcion': 'Martillos, destornilladores, llaves, alicates, etc.'},
                {'nombre': 'Herramientas Eléctricas', 'descripcion': 'Taladros, sierras eléctricas, lijadoras, etc.'},
                {'nombre': 'Herramientas de Medición', 'descripcion': 'Cintas métricas, niveles, calibradores, etc.'},
                {'nombre': 'Herramientas de Jardín', 'descripcion': 'Podadoras, palas, rastrillos, etc.'},
            ],
            'Materiales de Construcción': [
                {'nombre': 'Cemento y Concreto', 'descripcion': 'Cemento, mortero, concreto premezclado'},
                {'nombre': 'Madera y Tableros', 'descripcion': 'Madera contrachapada, MDF, tableros'},
                {'nombre': 'Ladrillos y Bloques', 'descripcion': 'Ladrillos, bloques de hormigón, piedras'},
                {'nombre': 'Arena y Grava', 'descripcion': 'Arena de construcción, grava, piedra triturada'},
            ],
            'Pinturas': [
                {'nombre': 'Pintura Interior', 'descripcion': 'Pintura para interiores, latex, acrílica'},
                {'nombre': 'Pintura Exterior', 'descripcion': 'Pintura para exteriores, impermeables'},
                {'nombre': 'Esmaltes', 'descripcion': 'Esmaltes sintéticos, al agua, para metal'},
                {'nombre': 'Barnices y Lacas', 'descripcion': 'Barnices, lacas, selladores de madera'},
            ],
            'Electricidad': [
                {'nombre': 'Cables y Conductores', 'descripcion': 'Cables eléctricos, alambres, conductores'},
                {'nombre': 'Interruptores y Enchufes', 'descripcion': 'Interruptores, tomacorrientes, cajas'},
                {'nombre': 'Iluminación', 'descripcion': 'Focos, lámparas, reflectores, LED'},
                {'nombre': 'Tableros y Protecciones', 'descripcion': 'Breakers, tableros eléctricos, fusibles'},
            ],
            'Plomería': [
                {'nombre': 'Tuberías', 'descripcion': 'Tuberías de PVC, cobre, galvanizadas'},
                {'nombre': 'Conexiones y Accesorios', 'descripcion': 'Codos, tees, uniones, válvulas'},
                {'nombre': 'Grifería', 'descripcion': 'Grifos, llaves de paso, mezcladoras'},
                {'nombre': 'Sanitarios', 'descripcion': 'Inodoros, lavabos, duchas, bañeras'},
            ],
            'Ferretería General': [
                {'nombre': 'Tornillos y Clavos', 'descripcion': 'Tornillos, clavos, pernos, tuercas'},
                {'nombre': 'Adhesivos y Selladores', 'descripcion': 'Pegamentos, silicona, cinta adhesiva'},
                {'nombre': 'Cerrajería', 'descripcion': 'Cerraduras, candados, bisagras, picaportes'},
                {'nombre': 'Abrasivos', 'descripcion': 'Lijas, discos de corte, piedras de afilar'},
            ],
            'Seguridad': [
                {'nombre': 'Equipos de Protección Personal', 'descripcion': 'Cascos, guantes, lentes, mascarillas'},
                {'nombre': 'Sistemas de Seguridad', 'descripcion': 'Cámaras, alarmas, sensores'},
                {'nombre': 'Señalización', 'descripcion': 'Señales de seguridad, conos, cintas'},
                {'nombre': 'Extintores y Primeros Auxilios', 'descripcion': 'Extintores, botiquines, mantas'},
            ],
        }

        categorias_creadas = 0
        subcategorias_creadas = 0

        for categoria_nombre, subcategorias_list in subcategorias_data.items():
            try:
                # Buscar o crear la categoría
                categoria, created = Categoria.objects.get_or_create(
                    nombre=categoria_nombre,
                    defaults={'activa': True}
                )
                
                if created:
                    categorias_creadas += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Categoría creada: {categoria_nombre}'))
                
                # Crear subcategorías
                for subcat_data in subcategorias_list:
                    subcategoria, sub_created = Subcategoria.objects.get_or_create(
                        nombre=subcat_data['nombre'],
                        categoria=categoria,
                        defaults={
                            'descripcion': subcat_data['descripcion'],
                            'activa': True
                        }
                    )
                    
                    if sub_created:
                        subcategorias_creadas += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Subcategoría creada: {subcat_data["nombre"]}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  - Subcategoría ya existe: {subcat_data["nombre"]}')
                        )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error con categoría {categoria_nombre}: {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS(f'\n===== RESUMEN ====='))
        self.stdout.write(self.style.SUCCESS(f'Categorías creadas: {categorias_creadas}'))
        self.stdout.write(self.style.SUCCESS(f'Subcategorías creadas: {subcategorias_creadas}'))
        self.stdout.write(self.style.SUCCESS(f'Proceso completado exitosamente!'))
