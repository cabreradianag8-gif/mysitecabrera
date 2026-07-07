from django.db import models
from proveedores.models import Proveedores
from productos.models import Producto
# Create your models here.
class Compras(models.Model):
    folio = models.CharField()
    fecha = models.DateField()
    subtotal=models.FloatField()
    iva=models.FloatField()
    total=models.FloatField()
    proveedor=models.ManyToManyField(Proveedores)
    producto=models.ManyToManyField(Producto)
#aj

