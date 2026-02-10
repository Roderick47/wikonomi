from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone

from Product.models import Product
from Comment.models import ProductComment, BusinessComment
from Follow.models import ProductSubscription, BusinessSubscription, UserFollow
from Post.models import Post, PostComment, PostLike
from QA.models import Answer, AnswerComment
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
    if instance.parent:
        # Notify the parent comment's author about the reply
        Notification.create_comment_reply_notification(
            comment=instance,
            parent_comment=instance.parent
        )
    
    # Notify all users who follow this product about the new comment
    # (excluding the comment author)
    followers = ProductSubscription.objects.filter(
        product=instance.product
    ).exclude(
        user=instance.user  # Don't notify the commenter about their own comment
    ).select_related('user')
    
    Notification.create_new_comment_notification(
        comment=instance,
        product_followers=followers
    )

@receiver(post_save, sender=ProductSubscription)
def notify_new_follower(sender, instance, created, **kwargs):
    """Notify product owners when someone follows their product."""
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

# --- New Notification Logic ---

@receiver(post_save, sender=UserFollow)
def notify_new_user_follower(sender, instance, created, **kwargs):
    """Notify a user when they are followed by another user."""
    if created:
        Notification.objects.create(
            user=instance.following,
            notification_type=Notification.NEW_FOLLOWER,
            data={'follower_username': instance.user.username}
        )

@receiver(post_save, sender=BusinessSubscription)
def notify_business_follower(sender, instance, created, **kwargs):
    """Notify business owner when someone follows their business."""
    if created and instance.business.author != instance.user:
        Notification.objects.create(
            user=instance.business.author,
            notification_type=Notification.NEW_FOLLOWER,
            business=instance.business,
            data={
                'follower_username': instance.user.username,
                'business_name': instance.business.name
            }
        )

@receiver(post_save, sender=PostComment)
def notify_post_comment(sender, instance, created, **kwargs):
    """Notify post author of comments, and parent author of replies."""
    if created and instance.is_active:
        # 1. Notify Post Author
        if instance.post.author != instance.user:
            Notification.objects.create(
                user=instance.post.author,
                notification_type=Notification.POST_COMMENT,
                post=instance.post,
                data={
                     'commenter_username': instance.user.username,
                     'comment_preview': instance.body[:100]
                }
            )
        
        # 2. Notify Parent Comment Author (if reply)
        if instance.parent and instance.parent.user != instance.user:
            # Avoid double notification if parent author is also post author?
            # Usually fine to receive both or distinct ones. 
            # If parent author IS post author, they get POST_COMMENT and POST_REPLY?
            # Let's keep distinct.
            Notification.objects.create(
                user=instance.parent.user,
                notification_type=Notification.POST_REPLY,
                post=instance.post,
                data={
                    'replier_username': instance.user.username,
                     'comment_preview': instance.body[:100]
                }
            )

@receiver(post_save, sender=PostLike)
def notify_post_like(sender, instance, created, **kwargs):
    """Notify post author of new likes."""
    # Notify if created=True or if effectively re-activated (is_active=True)
    if (created or instance.is_active) and instance.post.author != instance.user:
        # Check if a recent notification exists to avoid spam on toggle?
        # For simplicity, we trigger.
        Notification.objects.create(
            user=instance.post.author,
            notification_type=Notification.POST_LIKE,
            post=instance.post,
            data={'liker_username': instance.user.username}
        )

@receiver(pre_save, sender=Answer)
def track_answer_acceptance(sender, instance, **kwargs):
    """Track if answer is being accepted."""
    if instance.pk:
        try:
            old = Answer.objects.get(pk=instance.pk)
            instance._was_accepted = old.is_accepted
        except Answer.DoesNotExist:
            instance._was_accepted = False
    else:
        instance._was_accepted = False

@receiver(post_save, sender=Answer)
def notify_answer_accepted(sender, instance, created, **kwargs):
    """Notify answer author when their answer is accepted."""
    if not created and instance.is_accepted and not getattr(instance, '_was_accepted', False):
        if instance.author != instance.question.author:
             Notification.objects.create(
                user=instance.author,
                notification_type=Notification.ANSWER_ACCEPTED,
                answer=instance,
                question=instance.question,
                data={'accepter_username': instance.question.author.username}
             )

@receiver(post_save, sender=AnswerComment)
def notify_answer_comment(sender, instance, created, **kwargs):
    """Notify answer author of comments."""
    if created:
        if instance.answer.author != instance.user:
             Notification.objects.create(
                user=instance.answer.author,
                notification_type=Notification.ANSWER_COMMENT,
                answer=instance.answer,
                 question=instance.answer.question,
                data={
                    'commenter_username': instance.user.username,
                    'comment_preview': instance.body[:100]
                }
             )

@receiver(post_save, sender=BusinessComment)
def notify_business_comment(sender, instance, created, **kwargs):
    """Notify business owner of new comments/reviews."""
    if created and instance.is_active:
         # Notify Business Owner
         if instance.business.author != instance.user:
             Notification.objects.create(
                 user=instance.business.author,
                 notification_type=Notification.BUSINESS_REVIEW,
                 business=instance.business,
                 data={
                     'commenter_username': instance.user.username,
                      'comment_preview': instance.body[:100]
                 }
             )
         
         # Notify Parent (Reply)
         if instance.parent and instance.parent.user != instance.user:
             Notification.objects.create(
                 user=instance.parent.user,
                 notification_type=Notification.BUSINESS_REPLY,
                 business=instance.business,
                 data={
                     'replier_username': instance.user.username,
                      'comment_preview': instance.body[:100]
                 }
             )
