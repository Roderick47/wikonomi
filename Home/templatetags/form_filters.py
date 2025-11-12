from django import template
from django.forms import CheckboxInput, RadioSelect, Select, SelectMultiple

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a CSS class to a form field"""
    attrs = {}
    field_type = field.field.widget.__class__.__name__
    
    # Add base class
    if field_type in ['TextInput', 'PasswordInput', 'EmailInput', 'NumberInput', 'Textarea', 'DateInput', 'DateTimeInput', 'TimeInput', 'URLInput']:
        attrs['class'] = 'form-control'
    elif field_type in ['Select', 'SelectMultiple']:
        attrs['class'] = 'form-select'
    elif field_type in ['CheckboxInput', 'CheckboxSelectMultiple']:
        attrs['class'] = 'form-check-input'
    else:
        attrs['class'] = 'form-control'
    
    # Add any additional classes
    if css_class:
        attrs['class'] = f"{attrs['class']} {css_class}"
    
    # Apply attributes to the field
    return field.as_widget(attrs=attrs)
