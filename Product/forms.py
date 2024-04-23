from django import forms
from .models import Product

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['author','business','is_public','date_created','date_updated','location']


class GetOrCreateBusinessForm(forms.Form):
    business = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Who sells it?"}))