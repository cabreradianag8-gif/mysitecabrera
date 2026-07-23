from django.contrib import admin
from .models import nomina

class NominaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numperiodo', 'empleado', 'fecha', 'salario', 'percepciones', 'deducciones', 'total', 'status')
    search_fields = ('numperiodo', 'empleado__nombre', 'empleado__apellido')  
    list_filter = ('numperiodo', 'fecha', 'status')                           
    ordering = ('-id',)                                                        


admin.site.register(nomina, NominaAdmin)