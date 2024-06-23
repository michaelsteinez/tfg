from collections import defaultdict

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from modric.models import Comunidad, Partido


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def calcularEstadisticas(usuario):
    # https://stackoverflow.com/questions/31237042/whats-the-difference-between-select-related-and-prefetch-related-in-django-orm
    partidos_local = Partido.objects.filter(integrantes_local=usuario).select_related('deporte').prefetch_related(
        'integrantes_local', 'integrantes_visitante')
    partidos_visitante = Partido.objects.filter(integrantes_visitante=usuario).select_related(
        'deporte').prefetch_related('integrantes_local', 'integrantes_visitante')

    # Inicializamos
    estadisticas_por_deporte = defaultdict(lambda: {'ganados': 0, 'empatados': 0, 'perdidos': 0, 'total': 0})

    for partido in partidos_local:
        deporte = partido.deporte
        estadisticas_por_deporte[deporte]['total'] += 1
        if partido.resultado_estado == Partido.V:
            estadisticas_por_deporte[deporte]['ganados'] += 1
        elif partido.resultado_estado == Partido.E:
            estadisticas_por_deporte[deporte]['empatados'] += 1
        elif partido.resultado_estado == Partido.D:
            estadisticas_por_deporte[deporte]['perdidos'] += 1

    for partido in partidos_visitante:
        deporte = partido.deporte
        estadisticas_por_deporte[deporte]['total'] += 1
        if partido.resultado_estado == Partido.V:
            estadisticas_por_deporte[deporte]['perdidos'] += 1
        elif partido.resultado_estado == Partido.E:
            estadisticas_por_deporte[deporte]['empatados'] += 1
        elif partido.resultado_estado == Partido.D:
            estadisticas_por_deporte[deporte]['ganados'] += 1

    # Calcular porcentajes
    for deporte, stats in estadisticas_por_deporte.items():
        total = stats['total']
        if total > 0:
            stats['porcentaje_ganados'] = (stats['ganados'] / total) * 100
            stats['porcentaje_empatados'] = (stats['empatados'] / total) * 100
            stats['porcentaje_perdidos'] = (stats['perdidos'] / total) * 100
        else:
            stats['porcentaje_ganados'] = 0
            stats['porcentaje_empatados'] = 0
            stats['porcentaje_perdidos'] = 0

    return dict(estadisticas_por_deporte)


class VerPerfil(LoginRequiredMixin, TemplateView):
    template_name = "accounts/ver_perfil.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["usuario"] = self.request.user
        context["comunidades"] = Comunidad.objects.filter(miembros=self.request.user)
        context["estadisticas"] = calcularEstadisticas(self.request.user)

        return context


class EditarPerfil(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/editar_perfil.html"
    success_url = reverse_lazy("accounts:perfil")

    def get_object(self):
        return self.request.user

    # Esto es para que el campo fecha de nacimiento del formulario se inicialice correctamente (antes fallaba por el formato)
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.fecha_nac:
            initial['fecha_nac'] = self.request.user.fecha_nac.strftime('%Y-%m-%d')
        # print("Initial fecha_nac:", initial['fecha_nac'])  # Para ver el formato que debe ser YYYY-MM-DD
        return initial

    # Sobrescribir el método post para manejar archivos
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Sobrescribir form_valid para guardar el formulario correctamente
    def form_valid(self, form):
        form.instance = self.object
        form.save()
        return super().form_valid(form)
