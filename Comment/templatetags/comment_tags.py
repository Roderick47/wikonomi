from django import template
from ..utils import render_rich_text

register = template.Library()

@register.filter(name='rich_text')
def rich_text(text):
    return render_rich_text(text)
