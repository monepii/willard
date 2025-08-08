from django.db import models


class Blog(models.Model):
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='blog_images/', default='blog_images/default.jpg', blank=True, null=True)
    autor = models.CharField(max_length=100, default='Admin')
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-fecha']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', args=[str(self.id)])

