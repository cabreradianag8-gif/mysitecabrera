from django.db import models
from proveedores.models import Proveedores
from productos.models import Producto

class Compras(models.Model):
    # Opciones de estatus comercial
    ESTATUS_CHOICES = [
        ('Procesada', 'Procesada'),
        ('Cancelada', 'Cancelada'),
    ]

    folio = models.CharField(max_length=50)
    fecha = models.DateField()
    subtotal = models.FloatField()
    iva = models.FloatField()
    total = models.FloatField()
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='Procesada')
    
    # Declaramos ManyToMany usando la tabla intermedia explícita 'through'
    proveedor = models.ManyToManyField(Proveedores)
    producto = models.ManyToManyField(Producto, through='DetalleCompra')

    def __str__(self):
        return f"{self.folio} ({self.estatus})"

# Nueva tabla puente que resolverá las cantidades y costos por renglón
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    costo_compra = models.FloatField()

    def __str__(self):
        return f"{self.compra.folio} - {self.producto.nombre} x {self.cantidad}"
