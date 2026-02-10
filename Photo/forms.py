from django import forms
from .models import ProductPhoto, BusinessPhoto

class ProductPhotoAddForm(forms.ModelForm):
    class Meta:
        model = ProductPhoto
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control image-preview-input'}),
        }

class BusinessPhotoAddForm(forms.ModelForm):
    class Meta:
        model = BusinessPhoto
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control image-preview-input'}),
        }

class GetOrCreateBusinessForm(forms.Form):
    business = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Who sells it?"}))
