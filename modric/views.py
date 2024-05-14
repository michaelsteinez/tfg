from datetime import date, timezone
from random import randint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests

from modric.models import Partido
from .forms import PartidoForm
from accounts.models import CustomUser
import time


@login_required
def index(request):
    return render(request, 'modric/index.html')


@login_required
def crear_partido(request):
    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modric:index')  # Reemplaza 'lista_partidos' ('index') con el nombre de la URL de tu lista de partidos
    else:
        form = PartidoForm()
    return render(request, 'modric/crear_partido.html', {'form': form})


@login_required
def listar_partidos(request):
    consulta = Partido.objects.all() # Filtraremos por jugador cuando haya más partidos y jugadores
    return render(request, 'modric/listar_partidos.html', {"lista_partidos": consulta})


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
            personaje.email = "borrame@apistarwars.com"
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
