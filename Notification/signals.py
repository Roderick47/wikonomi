from django.db.models.signals import post_save
from django.core.signals import request_started
from django.dispatch import receiver
from Product.models import Product
from History.models import ProductHistory
from .models import Notification
from django.contrib.auth.models import User
from Comment.models import ProductComment
from Follow.models import ProductSubscription

# Notifications for products ###

# Notification if a product has been saved. Nothing if just created.
@receiver(post_save,sender=Product)
def ProductEditNotification(sender,instance,**kwargs):
    ph = ProductHistory.objects.filter(product=instance).order_by('id').last()
    if ph:
        if instance.author.username != ph.current_author:
            if instance.price != ph.price:
                change_value = (abs(instance.price-ph.price)/ph.price)*100
                if instance.price > ph.price:
                    rmessage = "'{product}' increased by {change_value}% to '{product_price}'"
                else:
                    rmessage = "'{product}' decreased by {change_value}% to '{product_price}'"
                    
                try:
                    user_to_notify = User.objects.get(username=ph.current_author)
                    fmessage = rmessage.format(product=instance.name,change_value=change_value,product_price=instance.price)
                    Notification.objects.create(user=user_to_notify,text=fmessage,product=instance)
                except User.DoesNotExist: pass
            else:
                try:
                    user_to_notify = User.objects.get(username=ph.current_author)
                    rmessage = "'{product}' has been edited by '{product_author}'.click to see changes."
                    fmessage = rmessage.format(product=instance.name,product_author=instance.author)
                    Notification.objects.create(user=user_to_notify,text=fmessage,product=instance)
                except User.DoesNotExist: pass



@receiver(post_save,sender=Product)
def FollowPriceChange(sender,instance,**kwargs):
    if instance.price_change():
        subscriptions = ProductSubscription.objects.filter(product=instance)
        rmessage =  "'{product}' price is now'{product_price}'.click to see changes."
        fmessage = rmessage.format(
            product=instance.name,
            product_price = instance.price, 
            product_author=instance.author
            )
        for subscription in subscriptions:
            Notification.objects.create(user= subscription.user, text=fmessage, product=instance)




# @receiver(request_started)
# def notification_is


### Notifications for comments ###
# notitification if a product has a commment.
# @receiver(post_save,sender=ProductComment)
# def ProductCommentNotification(sender,created,instance,**kwargs):
#     if created:
#         if comment.has_replies
#         comment = instance
    



