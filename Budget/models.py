from django.db import models
from django.contrib.auth.models import User
from Product.models import Product

# Create your models here.

class Budget(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Budget: {{self.title}}"