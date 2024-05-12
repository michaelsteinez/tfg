from django.shortcuts import render, redirect
from modric.models import Partido
from .forms import PartidoForm

# Create your views here.
def index(request):
    return render(request, 'modric/index.html')


def crear_partido(request):
    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Reemplaza 'lista_partidos' ('index') con el nombre de la URL de tu lista de partidos
    else:
        form = PartidoForm()
    return render(request, 'modric/crear_partido.html', {'form': form})
