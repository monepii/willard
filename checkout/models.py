from django.db import models
from django.contrib.auth.models import User
from ferretetia.models import Producto
import uuid
from datetime import datetime


class Orden(models.Model):
    """Modelo para representar una orden de compra"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero_orden = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordenes')
    
    # Información de envío
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField()
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20, blank=True)
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Estado y fechas
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    # Notas adicionales
    notas = models.TextField(blank=True, help_text="Comentarios especiales del cliente")
    
    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-creado']
    
    def __str__(self):
        return f"Orden #{self.numero_orden} - {self.usuario.username}"
    
    def save(self, *args, **kwargs):
        if not self.numero_orden:
            # Generar número de orden único
            self.numero_orden = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)


class ItemOrden(models.Model):
    """Modelo para representar un item dentro de una orden"""
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Item de Orden'
        verbose_name_plural = 'Items de Orden'
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - Orden #{self.orden.numero_orden}"
    
    def save(self, *args, **kwargs):
        # Calcular precio total automáticamente
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
