from django import forms
from .models import Question, Answer, AnswerComment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your question?'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide more details (optional)...'}),
        }

    tags_input = forms.CharField(
        required=False,
        label='Tags',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Add tags separated by commas (e.g., fruit, organic, local)',
            'id': 'tags-input',
            'hx-get': '/tag-autocomplete-htmx',
            'hx-trigger': 'keyup changed delay:300ms',
            'hx-target': '#tag-suggestions',
            'autocomplete': 'off'
        })
    )

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your answer...'}),
        }

class AnswerCommentForm(forms.ModelForm):
    class Meta:
        model = AnswerComment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a comment for clarification...'}),
        }
