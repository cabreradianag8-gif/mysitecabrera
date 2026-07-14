from django.db import models
from proveedores.models import Proveedores
from productos.models import Producto
from inventarios.models import Inventario  # Importamos tu app de Inventarios

class Compras(models.Model):
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
    
    # Muchos a Muchos con proveedores
    proveedor = models.ManyToManyField(Proveedores)
    
    # Muchos a Muchos con Producto usando la tabla intermedia explícita
    producto = models.ManyToManyField(Producto, through='DetalleCompra')

    def __str__(self):
        return f"{self.folio} ({self.estatus})"


# Tu tabla puente explícita adaptada para conectar con Inventarios
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    # El eslabón clave: conecta directamente el renglón con el stock de la sucursal
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    
    cantidad = models.IntegerField()
    costo_compra = models.FloatField()

    def __str__(self):
        return f"{self.compra.folio} - {self.producto.nombre} x {self.cantidad} en {self.inventario.sucursal.nombre}"