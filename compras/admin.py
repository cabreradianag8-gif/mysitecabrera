from django.contrib import admin
from .models import Compras, DetalleCompra

class ComprasAdmin(admin.ModelAdmin):
    list_display = ('id', 'folio', 'fecha', 'subtotal', 'iva', 'total', 'estatus')
    search_fields = ('folio',)
    list_filter = ('estatus', 'fecha')
    ordering = ('-id',)  


class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'compra', 'producto', 'inventario', 'cantidad', 'costo_compra')
    search_fields = ('compra__folio', 'producto__nombre')  
    list_filter = ('compra__estatus', 'inventario__sucursal')
    ordering = ('-id',)


admin.site.register(Compras, ComprasAdmin)
admin.site.register(DetalleCompra, DetalleCompraAdmin)