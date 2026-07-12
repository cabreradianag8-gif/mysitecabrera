from django.db import models
from clientes.models import Cliente
from productos.models import Producto

class Ventas(models.Model):
    ESTATUS_CHOICES = [
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    folio = models.CharField(max_length=50, unique=True)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='Completada')
    
    # Un cliente puede registrar múltiples ventas en el sistema
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mis_ventas')
    
    # Relación de Muchos a Muchos explícita usando la tabla intermedia DetalleVenta
    productos = models.ManyToManyField(Producto, through='DetalleVenta', related_name='ventas_asociadas')

    def __str__(self):
        return f"Venta {self.folio} - {self.cliente.nombre} ({self.estatus})"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.venta.folio} -> {self.producto.nombre} ({self.cantidad} pzs)"