from django.forms import ModelForm
from django import forms
from .models import Location

class LocationForm(forms.Form):
    latitude = forms.FloatField(
        label='Latitude', 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Latitude (e.g., -1.2921)',
            'step': 'any'
        })
    )
    longitude = forms.FloatField(
        label='Longitude', 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Longitude (e.g., 36.8219)',
            'step': 'any'
        })
    )
    use_browser_location = forms.BooleanField(
        label='Use my current location',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'use-browser-location'
        })
    )
    address = forms.CharField(
        label='Address',
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter address or location name'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        use_browser_location = cleaned_data.get('use_browser_location')
        address = cleaned_data.get('address')

        # Location is optional - only validate if user is trying to provide location
        # If they have coordinates, that's fine
        # If they have an address, that's fine
        # If they have nothing, that's also fine (product will be saved without location)
        
        # Only validate if user explicitly wants browser location but didn't provide coordinates
        if use_browser_location and (latitude is None or longitude is None):
            # Don't raise error - just clear the flag since geolocation was blocked
            cleaned_data['use_browser_location'] = False

        return cleaned_data

    def save_location(self):
        """Save the location data and return a Location object"""
        latitude = self.cleaned_data.get('latitude')
        longitude = self.cleaned_data.get('longitude')
        address = self.cleaned_data.get('address')

        # If we have coordinates, create or get existing location
        if latitude is not None and longitude is not None:
            location, created = Location.objects.get_or_create(
                latitude=latitude,
                longitude=longitude
            )
            return location
        
        # If we only have address, create location with null coordinates
        elif address:
            location = Location.objects.create(
                latitude=None,
                longitude=None
            )
            return location
        
        return None
