from django import forms
from .models import BugReport

class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['title', 'url_route', 'description', 'expected_behavior', 'screenshot']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'expected_behavior': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'url_route': 'Page URL',
        }
