from django.forms import ModelForm
from django import forms

class LocationForm(forms.Form):
    latitude = forms.FloatField(label='Latitude', required=False)
    longitude = forms.FloatField(label='Longitude', required=False)
