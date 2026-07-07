from django.db import models

class grupos_grupos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    fecha_creacion = models.DateField()
    estatus = models.BooleanField(default=True)


class grupos_usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50)
    passwd = models.CharField(max_length=50)
    correo = models.EmailField()
    
    
    grupo = models.ForeignKey(grupos_grupos, on_delete=models.CASCADE)