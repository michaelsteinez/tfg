from django.contrib import admin

from modric.models import Deporte, Recinto


# Register your models here.


class DeporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'num_jugadores', 'duracion_base')


class RecintoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'municipio', 'provincia', 'pais')


admin.site.register(Deporte, DeporteAdmin)
admin.site.register(Recinto, RecintoAdmin)
