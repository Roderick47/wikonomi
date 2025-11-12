from django import template

register = template.Library()

@register.filter(name='abs')
def absolute_value(value):
    """Return the absolute value of the input."""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return value

@register.filter(name='format_currency')
def format_currency(value):
    """Format a number as currency."""
    try:
        return f"${float(value):.2f}"
    except (ValueError, TypeError):
        return value

@register.filter(name='price_change_class')
def price_change_class(value):
    """Return appropriate CSS class based on price change."""
    try:
        if float(value) > 0:
            return 'text-danger'
        elif float(value) < 0:
            return 'text-success'
    except (ValueError, TypeError):
        pass
    return 'text-muted'
