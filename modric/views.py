from datetime import date, datetime, timedelta

from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError
from random import randint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import requests

from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from modric.models import Partido, Recinto, Comunidad, Invitacion, Notificacion
from .forms import PartidoForm, InvitacionForm
from accounts.models import CustomUser

# Importamos Q para combinar las condiciones de los filtros en las querysets
from django.db.models import Q


@login_required
def index(request):
    return render(request, 'modric/index.html')


@login_required
def crear_partido(request):
    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            partido = form.save(commit=False)
            username = request.user.username
            creador = CustomUser.objects.get(username=username)
            partido.creador = creador

            # Combina fecha y hora en un solo campo
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            fecha_hora = datetime.combine(fecha, hora)
            partido.fecha = make_aware(fecha_hora)

            partido.save()
            # Para guardar los campos ManyToMany
            form.save_m2m()
            return redirect('modric:ver_partidos')
    else:
        form = PartidoForm()
    return render(request, 'modric/partido_crear.html', {'form': form})


@login_required
def editar_partido(request, pk):
    usuario = request.user
    partido = get_object_or_404(Partido, pk=pk)

    if usuario in partido.administradores.all() or usuario == partido.creador:
        if request.method == 'POST':
            form = PartidoForm(request.POST, instance=partido)
            if form.is_valid():
                try:
                    partido = form.save(commit=False)
                    partido.creador = request.user

                    # Combina fecha y hora en un solo campo
                    fecha = form.cleaned_data['fecha']
                    hora = form.cleaned_data['hora']
                    fecha_hora = datetime.combine(fecha, hora)
                    partido.fecha = make_aware(fecha_hora)

                    partido.full_clean()  # Llama a clean() para las validaciones del modelo
                    partido.save()
                    form.save_m2m()  # Para guardar los campos ManyToMany
                    return redirect('modric:detalle_partido', pk=pk)
                except ValidationError as e:
                    form.add_error(None, e)  # Agregar errores al formulario
        else:
            # Inicializar el formulario con los valores actuales del partido
            initial_data = {
                'fecha': partido.fecha.date().isoformat(),
                'hora': partido.fecha.time(),
            }
            print(initial_data)
            form = PartidoForm(instance=partido, initial=initial_data)
        return render(request, 'modric/partido_editar.html', {'form': form, 'partido': partido})
    else:
        return redirect('modric:detalle_partido', pk)


def comprobar_inscripcion(usuario, partido):
    return usuario in partido.integrantes.all()


@login_required
def detalle_partido(request, pk):
    # Las dos asignaciones son equivalentes pero la segunda reenvia a Not Found
    # partido = Partido.objects.get(pk=id)
    partido = get_object_or_404(Partido, pk=pk)

    administradores = partido.administradores.all()
    integrantes_local = partido.integrantes_local.all()
    integrantes_visitantes = partido.integrantes_visitante.all()
    sinequipo = partido.integrantes.all()

    inscrito = comprobar_inscripcion(request.user, partido)

    # Comprobamos si el usuario es organizador o creador para ofrecerle editarlo
    edicion = request.user in administradores or request.user == partido.creador

    # Convertimos a conjuntos para poder hacer la diferencia
    integrantes_local_set = set(integrantes_local)
    integrantes_visitantes_set = set(integrantes_visitantes)

    # Calculamos los integrantes sin equipo
    sinequipo = set(sinequipo) - integrantes_local_set - integrantes_visitantes_set

    # Convertimos el conjunto resultante de nuevo a QuerySet (o lista)
    sinequipo = list(sinequipo)

    usuario = request.user

    # Si es un partido de ayer o anterior, no puede apuntarse.
    apuntable = True
    if partido.fecha.date() < timezone.now().date():
        apuntable = False


    return render(request, 'modric/partido_detalle.html', {
        'partido': partido,
        'administradores': administradores,
        'integrantes_local': integrantes_local,
        'integrantes_visitantes': integrantes_visitantes,
        'sinequipo': sinequipo,
        'edicion': edicion,
        'inscrito': inscrito,
        'usuario': usuario,
        'apuntable': apuntable,
    })


@login_required
def listar_partidos(request):
    # Obtener la fecha y hora actuales con soporte para zonas horarias para evitar el warning
    now = timezone.now()
    today = now.date()
    usuario = request.user

    # Definir el inicio del día de hoy y el inicio del día de mañana
    start_today = datetime.combine(today, datetime.min.time())
    start_today = timezone.make_aware(start_today, timezone.get_current_timezone())
    start_tomorrow = start_today + timedelta(days=1)

    # Filtrar los partidos anteriores a hoy (no incluye partidos de hoy)
    partidos_anteriores = Partido.objects.filter(fecha__lt=start_today).filter(
        Q(integrantes=usuario) | Q(creador=usuario)
    ).distinct().order_by('-fecha')

    # Filtrar los partidos de hoy (independientemente de la hora)
    partidos_hoy = Partido.objects.filter(fecha__gte=start_today, fecha__lt=start_tomorrow).filter(
        Q(integrantes=usuario) | Q(creador=usuario)
    ).distinct().order_by('fecha')

    # Filtrar los partidos futuros (después de hoy)
    partidos_futuros = Partido.objects.filter(fecha__gte=start_tomorrow).filter(
        Q(integrantes=usuario) | Q(creador=usuario)
    ).distinct().order_by('fecha')

    lista_no_inscritos = []
    for partido in partidos_futuros:
        if comprobar_inscripcion(request.user, partido):
            lista_no_inscritos.append(partido.id)

    return render(request, 'modric/partidos_listar.html', {
        "partidos_anteriores": partidos_anteriores,
        "partidos_hoy": partidos_hoy,
        "partidos_futuros": partidos_futuros,
        "usuario": usuario,
        "lista_no_inscritos": lista_no_inscritos,
    })


@login_required
def buscar_partidos(request):
    # Obtener la fecha y hora actuales con soporte para zonas horarias para evitar el warning
    now = timezone.now()
    usuario = request.user

    comunidades = Comunidad.objects.filter(miembros=usuario)

    # Filtrar los partidos sin comenzar en los que no estemos inscritos ya
    miscomunidades = Partido.objects.filter(fecha__gte=now).filter(comunidad__in=comunidades).filter(
        ~Q(integrantes=usuario)
    ).distinct().order_by('fecha')
    otros = Partido.objects.filter(fecha__gte=now).filter(visibilidad='A').filter(
        ~Q(comunidad__in=comunidades)).filter(~Q(integrantes=usuario)).distinct().order_by('fecha')

    return render(request, 'modric/partidos_buscar.html', {
        "miscomunidades": miscomunidades,
        "otros": otros,
        "usuario": usuario
    })


@login_required
def detalle_recinto(request, pk):
    recinto = get_object_or_404(Recinto, pk=pk)
    deportes = recinto.deportes.all()

    return render(request, 'modric/recinto.html', {
        'recinto': recinto,
        'deportes': deportes,
    })


def partido_in_out(usuario, partido, sentido):
    if sentido:
        partido.integrantes.add(usuario)
    else:
        partido.integrantes.remove(usuario)
        if usuario in partido.integrantes_local.all():
            partido.integrantes_local.remove(usuario)
        elif usuario in partido.integrantes_visitante.all():
            partido.integrantes_visitante.remove(usuario)

    return usuario in partido.integrantes.all()



def jugador_partido(request):
    partido_id = request.POST['partido_id']
    usuario_id = request.POST['usuario_id']
    sentido = request.POST['sentido']
    partido = Partido.objects.get(pk=partido_id)
    usuario = CustomUser.objects.get(pk=usuario_id)
    if sentido == 'in':
        sentido = True
    elif sentido == 'out':
        sentido = False
    else:
        redirect('modric:detalle_partido', pk=partido.id)

    partido_in_out(usuario, partido, sentido)

    return render(request, 'modric/inscribir_jugador.html', {
        'partido': partido,
        'jugador': usuario,
        'sentido': sentido
    })


@login_required
def enviar_invitacion(request):
    if request.method == 'POST':
        form = InvitacionForm(request.POST)
        if form.is_valid():
            invitacion = form.save()
            Notificacion.objects.create(
                usuario=invitacion.usuario,
                mensaje=f'Has sido invitado a unirte a la comunidad {invitacion.comunidad.nombre}.'
            )
            return redirect('modric:invitaciones_enviadas')
    else:
        form = InvitacionForm(user=request.user)
    return render(request, 'modric/enviar_invitacion.html', {'form': form})


@login_required
def solicitar_membresia(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    if request.method == 'POST':
        invitacion, created = Invitacion.objects.get_or_create(comunidad=comunidad, usuario=request.user)
        if created:
            Notificacion.objects.create(
                usuario=invitacion.comunidad.creador,
                mensaje=f'{request.user.username} ha solicitado unirse a la comunidad {invitacion.comunidad.nombre}.'
            )
        return redirect('modric:detalle_comunidad', comunidad_id=comunidad_id)
    return render(request, 'modric/solicitar_membresia.html', {'comunidad': comunidad})


@login_required
def manejar_solicitudes(request):
    invitaciones = Invitacion.objects.filter(comunidad__administradores=request.user, estado=Invitacion.PENDIENTE)
    if request.method == 'POST':
        invitacion_id = request.POST.get('invitacion_id')
        action = request.POST.get('action')
        invitacion = get_object_or_404(Invitacion, id=invitacion_id)
        if action == 'aceptar':
            invitacion.estado = Invitacion.ACEPTADA
            invitacion.comunidad.miembros.add(invitacion.usuario)
            Notificacion.objects.create(
                usuario=invitacion.usuario,
                mensaje=f'Tu solicitud de unirte a la comunidad {invitacion.comunidad.nombre} ha sido aceptada.'
            )
        elif action == 'rechazar':
            invitacion.estado = Invitacion.RECHAZADA
            Notificacion.objects.create(
                usuario=invitacion.usuario,
                mensaje=f'Tu solicitud de unirte a la comunidad {invitacion.comunidad.nombre} ha sido denegada.'
            )
        invitacion.save()
        return redirect('modric:manejar_solicitudes')
    return render(request, 'modric/manejar_solicitudes.html', {'invitaciones': invitaciones})


@login_required
def invitaciones_enviadas(request):
    invitaciones = Invitacion.objects.filter(comunidad__administradores=request.user)
    return render(request, 'modric/invitaciones_enviadas.html', {'invitaciones': invitaciones})



@login_required
def notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')
    if request.method == 'POST':
        notificacion_id = request.POST.get('notificacion_id')
        notificacion = get_object_or_404(Notificacion, id=notificacion_id)
        notificacion.leido = True
        notificacion.save()
        return redirect('modric:notificaciones')
    return render(request, 'modric/notificaciones.html', {'notificaciones': notificaciones})


@login_required
def detalle_comunidad(request, pk):
    comunidad = get_object_or_404(Comunidad, pk=pk)
    invitaciones = Invitacion.objects.filter(comunidad=comunidad)
    usuario = request.user
    return render(request, 'modric/comunidad_detalle.html', {'comunidad': comunidad,
                                                             'invitaciones': invitaciones,
                                                             'usuario': usuario})


class ComunidadesUsuarioView(LoginRequiredMixin, ListView):
    template_name = 'modric/comunidades_usuario.html'
    context_object_name = 'comunidades'

    def get_queryset(self):
        return Comunidad.objects.filter(miembros=self.request.user)


class ComunidadCrearView(LoginRequiredMixin, CreateView):
    model = Comunidad
    template_name = 'modric/comunidad_crear.html'

    fields = ['nombre', 'escudo', 'descripcion']
    success_url = reverse_lazy('accounts:perfil')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        response = super().form_valid(form)

        self.object.administradores.add(self.request.user)
        self.object.miembros.add(self.request.user)
        return response


class ComunidadEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comunidad
    template_name = 'modric/comunidad_editar.html'

    fields = ['nombre', 'escudo', 'descripcion', 'administradores', 'miembros']

    def get_success_url(self):
        return reverse('modric:detalle_comunidad', kwargs={'pk': self.object.pk})

    def test_func(self):
        comunidad = self.get_object()
        # Permitir acceso solo al creador o a los administradores
        if self.request.user == comunidad.creador or self.request.user in comunidad.administradores.all():
            return True
        raise PermissionDenied

    def form_valid(self, form):
        response = super().form_valid(form)
        comunidad = self.object

        if comunidad.creador not in comunidad.administradores.all():
            comunidad.administradores.add(comunidad.creador)
        if comunidad.creador not in comunidad.miembros.all():
            comunidad.miembros.add(comunidad.creador)

        for admin in comunidad.administradores.all():
            if admin not in comunidad.miembros.all():
                comunidad.miembros.add(admin)

        return response


# # Recibe objetos, no indices. Devuelve True si el jugador está entre los integrantes del partido.
# def comprobar_jugador_partido(usuario, partido):
#     if usuario in partido.integrantes.all():
#         return True
#     else:
#         return False
#
#
# # Devuelve True si el jugador se ha inscrito en el partido
# def partido_in(usuario_id, partido_id):
#     partido = Partido.objects.get(pk=partido_id)
#     usuario = CustomUser.objects.get(pk=usuario_id)
#
#     partido.integrantes.add(usuario)
#
#     return comprobar_jugador_partido(usuario, partido)
#
#
# # Devuelve True si el jugador se ha borrado del partido
# def partido_out(usuario_id, partido_id):
#     partido = Partido.objects.get(pk=partido_id)
#     usuario = CustomUser.objects.get(pk=usuario_id)
#
#     partido.integrantes.remove(usuario)
#
#     return not comprobar_jugador_partido(usuario, partido)


@login_required
def importar_usuarios_API(request):
    # Funcion pseudoaleatoria para generar fechas de nacimiento
    def generar_fecha_aleatoria():
        # Genera un año aleatorio entre 1970 y 2002
        año = randint(1970, 2002)
        # Genera un mes y un día aleatorios
        mes = randint(1, 12)
        dia = randint(1, 28)  # Usamos 28 como máximo para simplificar, ya que febrero puede tener 28 días

        # Crea un objeto datetime con la fecha aleatoria generada
        fecha_aleatoria = date(year=año, month=mes, day=dia)

        return fecha_aleatoria

    def obtener_personaje(id_personaje):
        url = f"https://www.swapi.tech/api/people/{id_personaje}"
        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            datos = respuesta.json()
            nombre = datos['result']['properties']['name']
            apellido = "API"
            altura = datos['result']['properties']['height']
            if altura == 'unknown':
                altura = '165'
            if datos['result']['properties']['gender'] == 'female':
                sexo = 'M'
            else:
                sexo = 'V'
            personaje = CustomUser()
            separar = nombre.split()

            personaje.username = separar[0]
            personaje.first_name = nombre
            personaje.last_name = apellido
            personaje.altura = altura
            personaje.sexo = sexo
            personaje.email = f"borrame{id_personaje}@apistarwars.com"
            personaje.fecha_nac = generar_fecha_aleatoria()

            personaje.save()

            return personaje
        else:
            print("Error al obtener datos:", respuesta.status_code)
            return None

    lista_personajes = []
    for cont in range(1, 30):
        personaje = obtener_personaje(cont)
        if personaje:
            lista_personajes.append(personaje)
    # print(lista_personajes)

    return render(request, 'modric/starwars.html', {"lista": lista_personajes})
