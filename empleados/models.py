from django.db import models

# Create your models here.
class empleados(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()
    telefono = models.CharField()
    email = models.EmailField()
    turno = models.CharField()
    status = models.BooleanField()

class nomina(models.Model):
    numperiodo = models.CharField()
    fecha=models.DateField()
    salario=models.FloatField()
    percepciones=models.FloatField()
    deducciones=models.FloatField()
    total=models.FloatField()
    empleado=models.ForeignKey(empleados, on_delete=models.CASCADE, related_name='nominas')

    