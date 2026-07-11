from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    estatus = models.BooleanField(default=True)  

    def __str__(self):
        return self.nombre
    