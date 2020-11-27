from django import forms
from django.forms import widgets
from .models import City


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control my-3',
                'placeholder': 'Enter City Name...'
            })
        }
        labels = {
            'name': '',
        }
