from django.db import models

class grupos_grupos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    fecha_creacion = models.DateField()
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    