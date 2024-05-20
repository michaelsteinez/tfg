from django import forms
from .models import Deporte, Partido


class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        # fields = '__all__'  # Por ahora, incluimos todos los campos del modelo
        # O seleccionamos los campos
        fields = ['deporte', 'fecha', 'duracion_personalizada', 'recinto', 'nombre_pista', 'cubierto',
                  'precio_pista', 'precio_jugador', 'administradores', 'integrantes',
                  'integrantes_local', 'integrantes_visitante', 'color_local', 'color_visitante', 'resultado_estado',
                  'marcador_local', 'marcador_visitante', 'visibilidad', 'comunidad']

