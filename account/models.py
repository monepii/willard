from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    id_personalizado = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=254)
    direccion = models.CharField(max_length=255, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_personalizado} - {self.nombre or self.user.username}"
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

class Direccion(models.Model):
    TIPO_DIRECCION_CHOICES = [
        ('casa', 'Casa'),
        ('trabajo', 'Trabajo'),
        ('otro', 'Otro'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direcciones')
    calle = models.CharField(max_length=200)
    numero_exterior = models.CharField(max_length=20)
    numero_interior = models.CharField(max_length=20, blank=True, null=True)
    colonia = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=100, default='México')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    instrucciones = models.TextField(blank=True, null=True, help_text="Instrucciones especiales de entrega")
    es_principal = models.BooleanField(default=False, help_text="Dirección principal de envío")
    activa = models.BooleanField(default=True)
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.calle} #{self.numero_exterior}, {self.colonia}"
    
    def save(self, *args, **kwargs):
        # Si se marca como principal, desmarcar las otras direcciones principales del usuario
        if self.es_principal:
            Direccion.objects.filter(user=self.user, es_principal=True).update(es_principal=False)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        ordering = ['-es_principal', '-creada']