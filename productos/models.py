from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.CharField()

