from django.db.models.signals import post_save
from django.core.signals import request_started
from django.dispatch import receiver
from Product.models import Product
from History.models import ProductHistory
from .models import Notification
from django.contrib.auth.models import User
from Comment.models import ProductComment
from .models import ProductSubscription

# Notifications for products ###

# Notification if a product has been saved. Nothing if just created.







    



