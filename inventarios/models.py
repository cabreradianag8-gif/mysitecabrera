from django.db import models
from productos.models import Producto
from proveedores.models import Proveedores # Tu clase en plural según tu foto
from sucursal.models import Sucursal

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    
    # Stock exclusivo por sucursal física
    stock_local = models.IntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'proveedor', 'sucursal')

    def __str__(self):
        return f"{self.producto.nombre} en {self.sucursal.nombre} ({self.stock_local} pzs)"