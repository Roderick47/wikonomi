from django import forms
from .models import Budget, BudgetCategory, BudgetItem
from Product.models import Product

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['title', 'description', 'period_type', 'start_date', 'end_date', 'target_amount']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Shopping, School Fees...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short description (optional)'}),
            'period_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = BudgetCategory
        fields = ['name', 'allocated_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Category Name'}),
            'allocated_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '0.00'}),
        }
