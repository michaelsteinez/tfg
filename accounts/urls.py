from django.urls import path

from .views import SignUpView, MiPerfil

app_name = 'accounts'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("perfil/", MiPerfil.as_view(), name="perfil"),
]
