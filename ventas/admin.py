from django.contrib import admin
from .models import Ventas, DetalleVenta

class VentasAdmin(admin.ModelAdmin):
    list_display = ('id', 'folio', 'fecha', 'cliente', 'sucursal', 'total', 'estatus')
    search_fields = ('folio', 'cliente__nombre', 'cliente__apellido', 'sucursal__nombre')
    list_filter = ('estatus', 'fecha', 'sucursal')
    ordering = ('-id',)  


class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'producto', 'cantidad')
    search_fields = ('venta__folio', 'producto__nombre')  
    list_filter = ('venta__estatus',)
    ordering = ('-id',)


admin.site.register(Ventas, VentasAdmin)
admin.site.register(DetalleVenta, DetalleVentaAdmin)