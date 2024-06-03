from django import forms
from .models import Partido, CustomUser


class PartidoForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha')
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Hora')

    class Meta:
        model = Partido

        fields = ['deporte', 'fecha', 'hora', 'duracion_personalizada', 'recinto', 'nombre_pista', 'cubierto',
                  'precio_pista', 'precio_jugador', 'administradores', 'integrantes',
                  'integrantes_local', 'integrantes_visitante', 'color_local', 'color_visitante', 'resultado_estado',
                  'marcador_local', 'marcador_visitante', 'visibilidad', 'comunidad']

    def __init__(self, *args, **kwargs):
        # Obtener la instancia del partido actual
        partido = kwargs.get('instance')
        super(PartidoForm, self).__init__(*args, **kwargs)

        if partido:
            # Filtrar los usuarios que forman parte de 'integrantes'
            self.fields['integrantes_local'].queryset = partido.integrantes.all()
            self.fields['integrantes_visitante'].queryset = partido.integrantes.all()
