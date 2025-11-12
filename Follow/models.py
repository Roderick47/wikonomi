from django.db import models
from Product.models import Product
from Business.models import Business
from django.contrib.auth.models import User
# Create your models here.

class ProductSubscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class BusinessSubscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business.name


class UserFollow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_set',  # Users that this user is following
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers_set',  # Users who follow this user
    )
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'following')  # Prevent duplicate follows
        verbose_name = 'User Follow'
        verbose_name_plural = 'User Follows'

    def __str__(self):
        return f"{self.user} follows {self.following}"
