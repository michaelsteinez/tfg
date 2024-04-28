from django.shortcuts import render, redirect
from .forms import RegistroForm


# Create your views here.
def index(request):
    return render(request, 'modric/index.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modric:registro_exito')  # Reemplaza 'registro_exitoso' con el nombre de la URL para la página de registro exitoso
    else:
        form = RegistroForm()
    return render(request, 'modric/registro.html', {'form': form})  # Reemplaza 'registro.html' con el nombre de tu template HTML de registro

def registro_exito(request):
    return render(request, 'modric/registro_exito.html')
