from django.db import models

class empleados(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    turno = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.nombre} {self.apellido}"