from django.urls import path
from modric.views import (index, crear_partido, buscar_partidos, listar_partidos, importar_usuarios_API,
                          detalle_partido, editar_partido, detalle_recinto, jugador_partido,
                          enviar_invitacion, solicitudes_grupos, solicitar_membresia, invitaciones_enviadas,
                          notificaciones, detalle_comunidad, solicitudes_personales, solicitudes_todas)
from modric import views

app_name = 'modric'

urlpatterns = [
    path('', index, name='index'),

    path('partidos/', listar_partidos, name='ver_partidos'),
    path('partido/buscar/', buscar_partidos, name='buscar_partidos'),
    path('partido/crear/', crear_partido, name='crear_partido'),
    path('partido/ver_detalle/<int:pk>/', detalle_partido, name='detalle_partido'),
    path('partido/editar/<int:pk>/', editar_partido, name='editar_partido'),

    path('partido/jugador_partido/', jugador_partido, name='jugador_partido'),

    path('recinto/<int:pk>/', detalle_recinto, name='recinto'),
    # Antes de descomentar las 2 URLs siguientes, descomentar en modric/views sus vistas correspondientes
    # e importar arriba
    # path('recinto/crear/', recinto_crear, name='recinto_crear'),
    # path('recinto/editar/<int:pk>/', recinto_editar, name='recinto_editar'),

    path('invitaciones/enviar/', enviar_invitacion, name='enviar_invitacion'),
    path('invitaciones/enviadas/', invitaciones_enviadas, name='invitaciones_enviadas'),

    path('solicitudes/', solicitudes_todas, name='solicitudes_todas'),
    path('solicitudes/grupos/', solicitudes_grupos, name='solicitudes_grupos'),
    path('solicitudes/personales/', solicitudes_personales, name='solicitudes_personales'),
    path('solicitar_membresia/<int:comunidad_id>/', solicitar_membresia, name='solicitar_membresia'),

    path('notificaciones/', notificaciones, name='notificaciones'),

    path('comunidad/<int:pk>/', detalle_comunidad, name='detalle_comunidad'),
    path('comunidades/', views.ComunidadesUsuarioView.as_view(), name='comunidades'),
    path('comunidad/crear/', views.ComunidadCrearView.as_view(), name='comunidad_crear'),
    path('comunidad/buscar/', views.ComunidadesBuscarNuevas.as_view(), name='comunidad_buscar'),
    path('comunidad/editar/<int:pk>/', views.ComunidadEditarView.as_view(), name='comunidad_editar'),

    path('starwars/', importar_usuarios_API, name='importar_starwars'),

    ]
