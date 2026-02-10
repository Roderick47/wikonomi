from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Business
from Location.forms import LocationForm

class BusinessAddForm(ModelForm):
    class Meta:
        model = Business
        fields = ['image','name', 'description', 'location_description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Business name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your business...',
                'rows': 3
            }),
            'location_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., "Next to the main mall, across from Starbucks"'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control image-preview-input'
            })
        }
    
    social_post = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Share a social post about your new business! (e.g., "We are open for business! Come visit us.")',
            'rows': 2,
            'maxlength': 500
        }),
        help_text="Optional: Create a social post to announce your business immediately."
    )

    tags_input = forms.CharField(
        required=False, 
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location_description'].help_text = "Provide a detailed description of where your business is located"

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


