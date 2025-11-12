from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from Product.models import Product
from Comment.models import ProductComment

User = get_user_model()

class Notification(models.Model):
    """
    Notification model for user notifications about product updates and comments.
    """
    # Notification types
    PRICE_CHANGE = 'price_change'
    PRICE_DROP = 'price_drop'
    COMMENT_REPLY = 'comment_reply'
    NEW_COMMENT = 'new_comment'
    
    NOTIFICATION_TYPES = [
        (PRICE_CHANGE, 'Price Change'),
        (PRICE_DROP, 'Price Drop'),
        (COMMENT_REPLY, 'Comment Reply'),
        (NEW_COMMENT, 'New Comment'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Related objects (only one of these should be set)
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    comment = models.ForeignKey(
        ProductComment, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    
    # Additional data stored as JSON
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"
        
    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
    
    @classmethod
    def create_price_change_notification(cls, user, product, old_price, new_price):
        """Create a price change notification."""
        change_percent = ((new_price - old_price) / old_price) * 100
        
        return cls.objects.create(
            user=user,
            notification_type=cls.PRICE_DROP if new_price < old_price else cls.PRICE_CHANGE,
            product=product,
            data={
                'old_price': str(old_price),
                'new_price': str(new_price),
                'change_percent': round(change_percent, 2)
            }
        )
    
    @classmethod
    def create_comment_reply_notification(cls, comment, parent_comment):
        """Create a notification for a comment reply."""
        if comment.author == parent_comment.author:
            return None  # Don't notify if replying to self
            
        return cls.objects.create(
            user=parent_comment.author,
            notification_type=cls.COMMENT_REPLY,
            product=comment.product,
            comment=comment,
            data={
                'replier_username': comment.author.username,
                'product_name': comment.product.name,
                'comment_preview': comment.content[:100]  # First 100 chars
            }
        )
    
    @classmethod
    def create_new_comment_notification(cls, comment, product_followers):
        """Create notifications for new comments on a product."""
        if not product_followers:
            return []
            
        notifications = []
        for follower in product_followers:
            if follower.user != comment.author:  # Don't notify self
                notifications.append(
                    cls(
                        user=follower.user,
                        notification_type=cls.NEW_COMMENT,
                        product=comment.product,
                        comment=comment,
                        data={
                            'commenter_username': comment.author.username,
                            'product_name': comment.product.name,
                            'comment_preview': comment.content[:100]
                        }
                    )
                )
        
        return cls.objects.bulk_create(notifications)

