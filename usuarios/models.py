from django.db import models
from grupos.models import grupos_grupos
from empleados.models import empleados as EmpleadoModel 

class grupos_usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50)
    passwd = models.CharField(max_length=50)
    correo = models.EmailField()
    
    # Relación 1 a Muchos
    grupo = models.ForeignKey(grupos_grupos, on_delete=models.PROTECT)
    
    # Relación 1 a 1 con tu clase de empleados
    empleado = models.OneToOneField(EmpleadoModel, on_delete=models.CASCADE, null=True, blank=True)

    estatus = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario