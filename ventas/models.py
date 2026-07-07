from django.db import models
from clientes.models import Cliente       # Importamos tu modelo de clientes
from productos.models import Producto  # Importamos tu modelo de productos

class Ventas(models.Model):
    folio = models.CharField(max_length=50, unique=True)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_length=10, max_digits=10, decimal_places=2)
    
    # RELACIÓN MUCHOS A MUCHOS: Un cliente puede tener muchas ventas, y una venta muchos productos
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto) # Genera la tabla relacional intermedia

    def __str__(self):
        return f"Venta Folio: {self.folio}"