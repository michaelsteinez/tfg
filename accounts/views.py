from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class VerPerfil(LoginRequiredMixin, TemplateView):
    template_name = "accounts/ver_perfil.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["usuario"] = self.request.user
        # context["usuario"] = CustomUser.objects.get(pk=usuario)

        return context


class EditarPerfil(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/editar_perfil.html"
    success_url = reverse_lazy("accounts:perfil")

    def get_object(self):
        return self.request.user

    # Esto es para que el campo fecha de nacimiento del formulario se inicialice correctamente
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.fecha_nac:
            initial['fecha_nac'] = self.request.user.fecha_nac.strftime('%Y-%m-%d')
        # print("Initial fecha_nac:", initial['fecha_nac'])  # Para ver el formato que debe ser YYYY-MM-DD
        return initial
