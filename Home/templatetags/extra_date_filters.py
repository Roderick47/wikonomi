from django import template
import datetime
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Max, Min
from Notification.models import Notification
from Product.models import Product

register = template.Library()

@register.filter(name="isNew")
def isNew(date):
    date3DaysAgo = datetime.date.today() - timedelta(days=3)
    isNew = date > date3DaysAgo 
    return isNew

@register.filter(name="isCheapest")
def isCheapest(product):
    label = ''
    # Check if the product has any tags
    if not hasattr(product, 'tags'):
        return label
        
    for tag in product.tags.all():
        # Get price statistics for products with this tag
        stats = tag.products.aggregate(
            min_price=Min('price'),
            avg_price=Avg('price'),
            max_price=Max('price')
        )
        
        # Skip if we don't have enough data
        if not all(stats.values()):
            continue
            
        # Check price conditions
        if product.price < 0.8 * float(stats['avg_price'] or 0):
            label = "cheap"
        if product.price == stats['min_price']:
            label = "cheapest-price"
        if product.price >= 1.3 * float(stats['avg_price'] or 0):
            label = "expensive"
        if product.price == stats['max_price']:
            label = "most-expensive"
            
    return label


@register.filter
def olderDate(date):
    prev24hours = timezone.now() - timedelta(hours=24)
    if date < prev24hours:
        return date.date()
    else:
        return date

@register.filter(name="anyNotification")
def anyNotification(user):
    """Return the count of unread notifications for the user."""
    if not user.is_authenticated:
        return 0
    return Notification.objects.filter(user=user, is_read=False).count()




