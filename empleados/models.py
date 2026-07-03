from django.db import models

# Create your models here.
class empleados(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()
    telefono = models.CharField()
    email = models.EmailField()
    turno = models.CharField()
    status = models.BooleanField()