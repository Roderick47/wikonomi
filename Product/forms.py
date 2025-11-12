from django import forms
from .models import Product

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['author','business','is_public','date_created','date_updated','location']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the product...',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            })
        }


class GetOrCreateBusinessForm(forms.Form):
    business = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Who sells it?",
            "class": "form-control"
        })
    )