from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone

from Product.models import Product
from Comment.models import ProductComment
from Follow.models import ProductSubscription
from .models import Notification

@receiver(pre_save, sender=Product)
def track_price_changes(sender, instance, **kwargs):
    """Track product price changes to notify followers."""
    if not instance.pk:
        return  # New product, no price change yet
        
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        instance._old_price = old_instance.price
    except sender.DoesNotExist:
        pass

@receiver(post_save, sender=Product)
def notify_price_changes(sender, instance, created, **kwargs):
    """Notify followers when a product's price changes."""
    if created or not hasattr(instance, '_old_price'):
        return
        
    if instance.price != instance._old_price:
        # Get all users who follow this product
        followers = ProductSubscription.objects.filter(
            product=instance
        ).select_related('user')
        
        # Create notifications in bulk
        notifications = []
        for subscription in followers:
            notifications.append(
                Notification.create_price_change_notification(
                    user=subscription.user,
                    product=instance,
                    old_price=instance._old_price,
                    new_price=instance.price
                )
            )
        
        # Clear the temporary attribute
        del instance._old_price

@receiver(post_save, sender=ProductComment)
def handle_comment_notifications(sender, instance, created, **kwargs):
    """Handle notifications for new comments and replies."""
    if not created:
        return
    
    # Handle comment replies
    if instance.parent_comment:
        # Notify the parent comment's author about the reply
        Notification.create_comment_reply_notification(
            comment=instance,
            parent_comment=instance.parent_comment
        )
    
    # Notify all users who follow this product about the new comment
    # (excluding the comment author)
    followers = ProductSubscription.objects.filter(
        product=instance.product
    ).exclude(
        user=instance.author  # Don't notify the commenter about their own comment
    ).select_related('user')
    
    Notification.create_new_comment_notification(
        comment=instance,
        product_followers=followers
    )

@receiver(post_save, sender=ProductSubscription)
def notify_new_follower(sender, instance, created, **kwargs):
    """(Optional) Notify product owners when someone follows their product."""
    if created and instance.product.author != instance.user:
        Notification.objects.create(
            user=instance.product.author,
            notification_type=Notification.NEW_FOLLOWER,
            product=instance.product,
            data={
                'follower_username': instance.user.username,
                'product_name': instance.product.name
            }
        )
