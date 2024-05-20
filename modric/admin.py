from django.contrib import admin

from modric.models import Deporte, Recinto, Partido, Comunidad


# Register your models here.


class DeporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'num_jugadores', 'duracion_base')


class RecintoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'municipio', 'provincia', 'pais')


class PartidoAdmin(admin.ModelAdmin):
    list_display = ('deporte', 'fecha', 'recinto', 'visibilidad', 'comunidad')
    fieldsets = (
        (None, {'fields': ('deporte', 'fecha', 'recinto', 'duracion_personalizada', 'visibilidad', 'comunidad')}),
        ('Información adicional', {'fields': ('nombre_pista', 'cubierto', 'precio_pista', 'precio_jugador',)}),
        ('Organización', {'fields': ('integrantes', 'integrantes_local', 'integrantes_visitante', 'color_local', 'color_visitante')}),
        ('Resultado', {'fields': ('resultado_estado', 'marcador_local', 'marcador_visitante')}),
    )


class ComunidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    ordering = ('fecha_creacion', 'nombre')
    fieldsets = (
        (None, {'fields': ('fecha_creacion', 'nombre')}),
        ('Información adicional', {'fields': ('descripcion', 'escudo')}),
        ('Organización', {'fields': ('administradores', 'miembros')}),
    )
    readonly_fields = ('fecha_creacion',)


admin.site.register(Deporte, DeporteAdmin)
admin.site.register(Recinto, RecintoAdmin)
admin.site.register(Partido, PartidoAdmin)
admin.site.register(Comunidad, ComunidadAdmin)
