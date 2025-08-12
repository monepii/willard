from django.db import models
from django.contrib.auth.models import User
from ferretetia.models import Producto


class Carrito(models.Model):
    """Modelo para representar un carrito de compras"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['-creado']

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def total_items(self):
        """Retorna el total de items en el carrito"""
        return sum(item.cantidad for item in self.items.all())

    @property
    def total_precio(self):
        """Retorna el precio total del carrito"""
        total = 0
        for item in self.items.all():
            # Usar el precio unitario guardado en el item
            total += item.cantidad * item.precio_unitario
        return total

    def limpiar(self):
        """Limpia todos los items del carrito"""
        self.items.all().delete()

    @staticmethod
    def obtener_o_crear_carrito(request):
        """Método estático para obtener o crear un carrito"""
        if request.user.is_authenticated:
            carrito, creado = Carrito.objects.get_or_create(
                usuario=request.user,
                activo=True
            )
            return carrito
        else:
            return None


class ItemCarrito(models.Model):
    """Modelo para representar un item en el carrito"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
        ordering = ['-creado']

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en {self.carrito}"

    @property
    def precio_total(self):
        """Retorna el precio total del item (cantidad * precio unitario)"""
        return self.cantidad * self.precio_unitario

    def actualizar_precio(self):
        """Actualiza el precio unitario basado en el producto"""
        if self.producto.descuento and self.producto.precioDescuento:
            self.precio_unitario = self.producto.precioDescuento
        else:
            self.precio_unitario = self.producto.precio
        self.save()

    def save(self, *args, **kwargs):
        """Sobrescribe save para actualizar automáticamente el precio"""
        if not self.precio_unitario:
            if self.producto.descuento and self.producto.precioDescuento:
                self.precio_unitario = self.producto.precioDescuento
            else:
                self.precio_unitario = self.producto.precio
        super().save(*args, **kwargs)
