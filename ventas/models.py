from django.db import models
from clientes.models import Cliente
from productos.models import Producto
from sucursal.models import Sucursal  # <-- IMPORTANTE: Importar tu app sucursal

class Ventas(models.Model):
    ESTATUS_CHOICES = [
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    folio = models.CharField(max_length=50, unique=True)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='Completada')
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mis_ventas')
    # Añadimos la sucursal obligatoria para el descuento de inventario regional
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='ventas_sucursal', null=True, blank=True)
    
    productos = models.ManyToManyField(Producto, through='DetalleVenta', related_name='ventas_asociadas')

    def __str__(self):
        return f"Venta {self.folio} - {self.cliente.nombre} ({self.estatus})"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.venta.folio} -> {self.producto.nombre} ({self.cantidad} pzs)"