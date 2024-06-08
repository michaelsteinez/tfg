from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class MiPerfil(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/perfil.html"
    success_url = reverse_lazy("perfil")

    def get_object(self):
        return self.request.user
