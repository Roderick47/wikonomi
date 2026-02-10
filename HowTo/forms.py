from django import forms
from .models import HowTo, HowToStep

class HowToForm(forms.ModelForm):
    class Meta:
        model = HowTo
        fields = ['title', 'description', 'business', 'product', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is this process called?'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Summarize the process...', 'rows': 3}),
            'business': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class HowToStepForm(forms.ModelForm):
    class Meta:
        model = HowToStep
        fields = ['title', 'content', 'image', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Step Title (Optional)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Explain what to do in this step...', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control image-preview-input'}),
            'order': forms.HiddenInput(),
        }
