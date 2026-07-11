from django.db import models
from empleados.models import empleados  

class nomina(models.Model):
    numperiodo = models.CharField(max_length=50)
    fecha = models.DateField()
    # Usamos DecimalField para precisión matemática exacta en dinero
    salario = models.DecimalField(max_digits=20, decimal_places=2)
    percepciones = models.DecimalField(max_digits=20, decimal_places=2)
    deducciones = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Tu relación de Clave Foránea exacta
    empleado = models.ForeignKey(empleados, on_delete=models.CASCADE, related_name='nominas')
    status = models.BooleanField(default=True)  

    def __str__(self):
        return f"Periodo {self.numperiodo} - {self.empleado.nombre}"