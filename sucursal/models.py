from django.db import models
from empleados.models import empleados  

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    
    personal = models.ManyToManyField(empleados, related_name='sucursales', blank=True)
    status = models.BooleanField(default=True)  

    def __str__(self):
        return self.nombre