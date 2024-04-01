from django.db import models
from Product.models import Product
from django.contrib.auth.models import User
# Create your models here.

class ProductSubscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name