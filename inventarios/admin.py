from django.contrib import admin
from .models import Inventario

class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'sucursal', 'cantidad', 'stock_minimo', 'estatus')
    search_fields = ('producto__nombre', 'sucursal__nombre')  
    list_filter = ('sucursal', 'estatus')                     
    ordering = ('id',)


admin.site.register(Inventario, InventarioAdmin)