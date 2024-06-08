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

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
                field.label_suffix = ''
                self.fields[field_name].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
            else:
                if field.widget.attrs.get('class'):
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

        if partido:
            # Filtrar los usuarios que forman parte de 'integrantes'
            self.fields['integrantes_local'].queryset = partido.integrantes.all()
            self.fields['integrantes_visitante'].queryset = partido.integrantes.all()
