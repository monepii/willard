from django.db import models
from django.contrib.auth.models import User
from ferretetia.models import Producto

# Create your models here.

class WishlistItem(models.Model):
    """Modelo para los elementos de la lista de deseos"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='wishlist_items')
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'producto']
        ordering = ['-fecha_agregado']
        verbose_name = 'Elemento de Lista de Deseos'
        verbose_name_plural = 'Elementos de Lista de Deseos'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"
