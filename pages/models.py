from django.db import models
from django.contrib.auth.models import AbstractUser
from random import choice

class Ropa(models.Model):
    Titulo = models.CharField(max_length=255)
    Marca = models.CharField (max_length= 100)
    Fecha_publicacion = models.DateTimeField()
    precio = models.IntegerField()
    image_url = models.CharField(max_length=2083, default="https://static.wixstatic.com/media/6deace_63ad94bb10b44aa5b9828a67fb9e75f8~mv2.jpg/v1/fill/w_500,h_500,al_c,lg_1,q_80,enc_auto/6deace_63ad94bb10b44aa5b9828a67fb9e75f8~mv2.jpg")


    def _str_(self):
        return self.titulo
    

class Regalo(models.Model):
    titulo_regalo=models.CharField(max_length=100)
    contenido_regalo=models.TextField()
    fecha_creacion=models.DateTimeField()
    fecha_modificacion=models.DateTimeField()


    def _str_(self):
        return self.titulo_nota
    

class Review(models.Model):
    Titulo_Review = models.CharField(max_length = 100)
    Contenido_Review = models.TextField()
    Fecha_Review = models.DateTimeField()



class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('Tienda', 'Tienda'),
        ('Cliente', 'Cliente'),
    ]
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO_CHOICES)
    
    # Agrega estos campos con related_name único
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    
class Recordatorio(models.Model):
    titulo = models.CharField(max_length = 40)
    nota_adicional = models.TextField()
    fecha = models.DateTimeField()
    