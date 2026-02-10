from django import template
from ..models import PostLike

register = template.Library()

@register.filter
def user_has_liked(post, user):
    """Check if a user has liked a post"""
    if not user.is_authenticated:
        return False
    return PostLike.objects.filter(post=post, user=user, is_active=True).exists()

@register.simple_tag(takes_context=True)
def get_user_like_status(context, post):
    request = context['request']
    if not request.user.is_authenticated:
        return False
    return PostLike.objects.filter(post=post, user=request.user, is_active=True).exists()
