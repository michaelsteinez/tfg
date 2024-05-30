from django import forms
from .models import Partido


class PartidoForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha')
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Hora')

    class Meta:
        model = Partido

        fields = ['deporte', 'fecha', 'hora', 'duracion_personalizada', 'recinto', 'nombre_pista', 'cubierto',
                  'precio_pista', 'precio_jugador', 'administradores', 'integrantes',
                  'integrantes_local', 'integrantes_visitante', 'color_local', 'color_visitante', 'resultado_estado',
                  'marcador_local', 'marcador_visitante', 'visibilidad', 'comunidad']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )