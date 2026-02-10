from django import forms
from .models import Post, PostComment


class PostForm(forms.ModelForm):
    """Form for creating/editing posts"""
    
    class Meta:
        model = Post
        fields = ['body', 'product', 'business']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': "What's on your mind? Share your thoughts...",
                'maxlength': 500,
            }),
            'product': forms.HiddenInput(),
            'business': forms.HiddenInput(),
        }
        labels = {
            'body': '',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        business = cleaned_data.get('business')
        
        # Ensure either product or business is set, not both
        if product and business:
            raise forms.ValidationError("A post can only reference a product OR a business, not both.")
        
        return cleaned_data


class PostCommentForm(forms.ModelForm):
    """Form for creating comments on posts"""
    
    class Meta:
        model = PostComment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Write a comment...',
                'maxlength': 500,
            }),
        }
        labels = {
            'body': '',
        }
