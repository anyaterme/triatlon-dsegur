from django import forms
from django.utils import timezone
from .models import IncidentForm

class IncidentFormForm(forms.ModelForm):
    class Meta:
        model = IncidentForm
        fields = '__all__'
        exclude= ['date_submitted', 'uuid', 'talon_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        fecha = cleaned.get('date')
        if fecha and fecha > timezone.now().date():
            self.add_error('date', 'La fecha no puede ser futura.')
        return cleaned