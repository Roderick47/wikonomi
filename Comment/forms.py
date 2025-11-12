from django import forms
from .models import ProductComment, BusinessComment, InfoComment

class CommentForm(forms.ModelForm):
    """Base comment form"""
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Write your comment...',
            'maxlength': 500
        }),
        max_length=500,
        help_text='Maximum 500 characters'
    )
    
    class Meta:
        model = None  # Will be set by subclasses
        fields = ['body']

class ProductCommentForm(CommentForm):
    """Form for product comments"""
    class Meta(CommentForm.Meta):
        model = ProductComment
        fields = ['body']

class BusinessCommentForm(CommentForm):
    """Form for business comments"""
    class Meta(CommentForm.Meta):
        model = BusinessComment
        fields = ['body']

class InfoCommentForm(CommentForm):
    """Form for info comments"""
    class Meta(CommentForm.Meta):
        model = InfoComment
        fields = ['body']

class ReplyForm(forms.Form):
    """Form for replies to comments"""
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Write your reply...',
            'maxlength': 500
        }),
        max_length=500,
        help_text='Maximum 500 characters'
    ) 