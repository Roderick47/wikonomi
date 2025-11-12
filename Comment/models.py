from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Product.models import Product
from Business.models import Business
from Information.models import Info

# Create your models here.

class Comment(models.Model):
    """Base comment model that can be used for products, businesses, or info"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_comments')
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.body[:50]}..."

    @property
    def is_reply(self):
        return self.parent is not None

    @property
    def reply_count(self):
        return self.replies.filter(is_active=True).count()

    @property
    def all_replies(self):
        return self.replies.filter(is_active=True).order_by('created_at')

    def get_reply_text(self):
        if self.reply_count == 0:
            return ""
        elif self.reply_count == 1:
            return "1 reply"
        else:
            return f"{self.reply_count} replies"

class ProductComment(Comment):
    """Comments for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    
    class Meta:
        ordering = ['-created_at']

class BusinessComment(Comment):
    """Comments for businesses"""
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='comments')
    
    class Meta:
        ordering = ['-created_at']

class InfoComment(Comment):
    """Comments for information posts"""
    info = models.ForeignKey(Info, on_delete=models.CASCADE, related_name='comments')
    
    class Meta:
        ordering = ['-created_at']
