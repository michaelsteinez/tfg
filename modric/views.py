from datetime import date, datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from random import randint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import requests

from modric.models import Partido, Recinto
from .forms import PartidoForm
from accounts.models import CustomUser
import time
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
    return render(request, 'modric/crear_partido.html', {'form': form})


@login_required
def editar_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)

    if request.method == 'POST':
        form = PartidoForm(request.POST, instance=partido)
        if form.is_valid():
            partido = form.save(commit=False)
            partido.creador = request.user

            # Combina fecha y hora en un solo campo
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            fecha_hora = datetime.combine(fecha, hora)

            # Asegúrate de que el datetime es consciente de la zona horaria
            partido.fecha = make_aware(fecha_hora)

            partido.save()
            form.save_m2m()  # Para guardar los campos ManyToMany
            return redirect('modric:index')  # Asegúrate de que 'modric:index' sea el nombre correcto de tu URL de éxito
    else:
        # Inicializar el formulario con los valores actuales del partido
        initial_data = {
            'fecha': partido.fecha.date().isoformat(),
            'hora': partido.fecha.time(),
        }
        print(initial_data)
        form = PartidoForm(instance=partido, initial=initial_data)

    return render(request, 'modric/editar_partido.html', {'form': form, 'partido': partido})

@login_required
def detalle_partido(request, pk):
    # Las dos asignaciones son equivalentes pero la segunda reenvia a Not Found
    # partido = Partido.objects.get(pk=id)
    partido = get_object_or_404(Partido, pk=pk)

    administradores = partido.administradores.all()
    integrantes_local = partido.integrantes_local.all()
    integrantes_visitantes = partido.integrantes_visitante.all()
    sinequipo = partido.integrantes.all()

    # Comprobamos si el usuario es organizador o creador para ofrecerle editarlo
    edicion = request.user in administradores or request.user == partido.creador

    # Convertimos a conjuntos para poder hacer la diferencia
    integrantes_local_set = set(integrantes_local)
    integrantes_visitantes_set = set(integrantes_visitantes)

    # Calculamos los integrantes sin equipo
    sinequipo = set(sinequipo) - integrantes_local_set - integrantes_visitantes_set

    # Convertimos el conjunto resultante de nuevo a QuerySet (o lista)
    sinequipo = list(sinequipo)

    return render(request, 'modric/detalle_partido.html', {
        'partido': partido,
        'administradores': administradores,
        'integrantes_local': integrantes_local,
        'integrantes_visitantes': integrantes_visitantes,
        'sinequipo': sinequipo,
        'edicion': edicion
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

    return render(request, 'modric/listar_partidos.html', {
        "partidos_anteriores": partidos_anteriores,
        "partidos_hoy": partidos_hoy,
        "partidos_futuros": partidos_futuros,
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
