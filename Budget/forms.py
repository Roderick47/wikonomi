from django import forms
from .models import Budget
from Product.models import Product

class BudgetAddForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2-multiple',
            'data-placeholder': 'Search and select products...',
            'style': 'width: 100%',
        }),
        required=False
    )
    
    class Meta:
        model = Budget
        fields = ['title', 'products']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter budget title...'
            }),
        }


