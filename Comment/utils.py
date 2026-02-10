import markdown
import bleach
from django.utils.safestring import mark_safe

def render_rich_text(text):
    if not text:
        return ""
    
    # 1. Convert Markdown to HTML
    # nl2br handles line breaks, sane_lists handles lists
    html = markdown.markdown(text, extensions=['nl2br', 'sane_lists'])
    
    # 2. Define safe tags and attributes
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'b', 'i', 
        'ul', 'ol', 'li', 'a', 'code', 'pre',
        'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'target'],
        'code': ['class'],
    }
    
    # 3. Sanitize the HTML
    clean_html = bleach.clean(
        html, 
        tags=allowed_tags, 
        attributes=allowed_attrs,
        strip=True
    )
    
    # 4. Auto-link URLs
    clean_html = bleach.linkify(clean_html)
    
    return mark_safe(clean_html)
