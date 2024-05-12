from django.contrib import admin

from modric.models import Deporte, Recinto, Partido


# Register your models here.


class DeporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'num_jugadores', 'duracion_base')


class RecintoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'municipio', 'provincia', 'pais')


class PartidoAdmin(admin.ModelAdmin):
    list_display = ('deporte', 'fecha', 'recinto')
    fieldsets = (
        (None, {'fields': ('deporte', 'fecha', 'recinto', 'duracion_personalizada')}),
        ('Información adicional', {'fields': ('nombre_pista', 'cubierto', 'precio_pista', 'precio_jugador',)}),
        ('Organización', {'fields': ('integrantes', 'integrantes_local', 'integrantes_visitante', 'color_local', 'color_visitante')}),
        ('Resultado', {'fields': ('resultado_estado', 'marcador_local', 'marcador_visitante')}),
    )

admin.site.register(Deporte, DeporteAdmin)
admin.site.register(Recinto, RecintoAdmin)
admin.site.register(Partido, PartidoAdmin)
