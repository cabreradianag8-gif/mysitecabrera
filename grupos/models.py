from django.db import models

class grupos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    fecha_creacion = models.DateField()
    estatus = models.BooleanField(default=True)

