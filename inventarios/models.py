from django.db import models
from productos.models import Producto
# Asumiendo que tu app se llama sucursal y el modelo Sucursal
from sucursal.models import Sucursal 

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    estatus = models.BooleanField(default=True)

    class Meta:
        # Evita que se duplique el mismo producto en la misma sucursal
        unique_together = ('producto', 'sucursal') 

    def __str__(self):
        return f"{self.producto.nombre} - {self.sucursal.nombre} ({self.cantidad} pzas)"