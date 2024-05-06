from django import forms
from .models import Budget

class BudgetAddForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['title','products']


