from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()
    sexo = models.CharField()
    tipo=models.CharField()
    direccion=models.CharField()
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"