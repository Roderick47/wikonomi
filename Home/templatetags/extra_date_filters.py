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
    for tag in product.tag_set.all():
        lowest_price = tag.products.aggregate(Min('price'))
        average_price = tag.products.aggregate(Avg('price'))
        highest_price = tag.products.aggregate(Max('price'))
        if product.price < 0.8*int(average_price['price__avg']):
            label = "cheap"
        if product.price == lowest_price['price__min']:
            label = "cheapest-price"
        if product.price >= 1.3*int(average_price['price__avg']):
            label = "expensive"
        if product.price == highest_price['price__max']:
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
    anyNotificationCount = Notification.objects.filter(user=user).filter(is_viewed=False).count()
    return anyNotificationCount




