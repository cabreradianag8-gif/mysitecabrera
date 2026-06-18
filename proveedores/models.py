from django.db import models

# Create your models here.
class Proveedores(models.Model):
    nombre = models.CharField()
    direccion = models.CharField()
    telefono = models.CharField()
    email = models.EmailField()
    categoria = models.CharField()