from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Business

class BusinessAddForm(ModelForm):
    class Meta:
        model = Business
        fields = ['image','name', 'description', 'location']


