from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from Product.models import Product
from Business.models import Business


class Post(models.Model):
    """
    Social post model that allows users to share their thoughts/commentary 
    about a Product or Business, similar to a tweet with embedded content.
    """
    # Author
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    # Post content/commentary
    body = models.TextField(max_length=500, help_text="Share your thoughts (max 500 characters)")
    
    # Optional: Reference to Product or Business (one or the other, not both)
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='posts',
        help_text="Product this post is about"
    )
    business = models.ForeignKey(
        Business, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='posts',
        help_text="Business this post is about"
    )
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Engagement metrics
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        content_type = "Product" if self.product else "Business" if self.business else "Generic"
        return f"{self.author.username}'s post about {content_type}: {self.body[:50]}..."
    
    def get_absolute_url(self):
        return reverse('Post:detail', kwargs={'post_id': self.pk})
    
    @property
    def content_object(self):
        """Returns the Product or Business this post is about"""
        return self.product or self.business
    
    @property
    def content_type_name(self):
        """Returns 'product' or 'business' or 'none'"""
        if self.product:
            return 'product'
        elif self.business:
            return 'business'
        return 'none'
    
    @property
    def like_count(self):
        """Count of likes"""
        return self.likes.filter(is_active=True).count()
    
    @property
    def comment_count(self):
        """Count of comments"""
        return self.comments.filter(is_active=True).count()
    
    def user_has_liked(self, user):
        """Check if a user has liked this post"""
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user, is_active=True).exists()
    
    def clean(self):
        """Ensure a post references either a product OR business, not both"""
        from django.core.exceptions import ValidationError
        if self.product and self.business:
            raise ValidationError("A post cannot reference both a product and a business")


class PostLike(models.Model):
    """Like model for posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class PostComment(models.Model):
    """Comment model for posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField(max_length=500)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.body[:50]}..."
    
    @property
    def is_reply(self):
        return self.parent is not None
    
    @property
    def reply_count(self):
        """Count all descendants recursively"""
        count = 0
        direct_replies = self.replies.filter(is_active=True)
        for reply in direct_replies:
            count += 1
            count += reply.reply_count
        return count
