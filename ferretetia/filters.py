import django_filters
from django_filters import CharFilter, NumberFilter, BooleanFilter, ChoiceFilter
from django.db import models
from .models import Producto, Categoria


class ProductoFilter(django_filters.FilterSet):
    """
    Filtro para productos con múltiples opciones de búsqueda
    """
    # Filtro de búsqueda por nombre y descripción
    search = CharFilter(
        method='filter_search',
        label='Buscar',
        help_text='Buscar por nombre o descripción del producto'
    )
    
    # Filtro por rango de precios
    precio_min = NumberFilter(
        field_name='precio',
        lookup_expr='gte',
        label='Precio mínimo'
    )
    precio_max = NumberFilter(
        field_name='precio',
        lookup_expr='lte',
        label='Precio máximo'
    )
    
    # Filtro por categoría
    categoria = django_filters.ModelChoiceFilter(
        queryset=Categoria.objects.filter(activa=True),
        label='Categoría'
    )
    
    # Filtro por disponibilidad
    disponible = BooleanFilter(
        label='Solo disponibles'
    )
    
    # Filtro por productos con descuento
    con_descuento = BooleanFilter(
        method='filter_con_descuento',
        label='Solo con descuento'
    )
    
    # Filtro por stock
    stock_min = NumberFilter(
        field_name='stock',
        lookup_expr='gte',
        label='Stock mínimo'
    )
    
    # Ordenamiento
    ordenar = ChoiceFilter(
        choices=[
            ('nombre', 'Nombre A-Z'),
            ('-nombre', 'Nombre Z-A'),
            ('precio', 'Precio menor a mayor'),
            ('-precio', 'Precio mayor a menor'),
            ('-creado', 'Más recientes'),
            ('creado', 'Más antiguos'),
        ],
        method='filter_ordenar',
        label='Ordenar por'
    )
    
    class Meta:
        model = Producto
        fields = {
            'nombre': ['icontains'],
            'categoria': ['exact'],
            'precio': ['gte', 'lte'],
            'disponible': ['exact'],
            'stock': ['gte'],
        }
    
    def filter_search(self, queryset, name, value):
        """
        Filtro personalizado para búsqueda en nombre y descripción
        """
        if value:
            return queryset.filter(
                models.Q(nombre__icontains=value) |
                models.Q(descripcion__icontains=value) |
                models.Q(sku__icontains=value)
            )
        return queryset
    
    def filter_con_descuento(self, queryset, name, value):
        """
        Filtro personalizado para productos con descuento
        """
        if value:
            return queryset.filter(descuento=True, precioDescuento__isnull=False)
        return queryset
    
    def filter_ordenar(self, queryset, name, value):
        """
        Filtro personalizado para ordenamiento
        """
        if value:
            return queryset.order_by(value)
        return queryset.order_by('-creado')  # Orden por defecto
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels y placeholders
        self.filters['nombre__icontains'].label = 'Nombre del producto'
        self.filters['nombre__icontains'].field.widget.attrs.update({
            'placeholder': 'Buscar por nombre...'
        })
        
        # Hacer algunos campos opcionales
        self.filters['precio_min'].field.required = False
        self.filters['precio_max'].field.required = False
        self.filters['stock_min'].field.required = False


class CategoriaFilter(django_filters.FilterSet):
    """
    Filtro para categorías
    """
    nombre = CharFilter(
        lookup_expr='icontains',
        label='Nombre de categoría'
    )
    
    activa = BooleanFilter(
        label='Solo categorías activas'
    )
    
    class Meta:
        model = Categoria
        fields = ['nombre', 'activa']

