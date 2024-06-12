from django.urls import path

from .views import SignUpView, VerPerfil, EditarPerfil

app_name = 'accounts'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("perfil/", VerPerfil.as_view(), name="perfil"),
    path("perfil/<int:id>/", VerPerfil.as_view(), name="ver_perfil"),
    path("perfil/editar/", EditarPerfil.as_view(), name="editar_perfil"),
]
