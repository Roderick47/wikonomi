from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from Business.models import Business
from Comment.models import ProductComment,BusinessComment


# Create your models here.
class Notification(models.Model):
    text = models.CharField(max_length=300)
    is_viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True, blank=True)
    business = models.ForeignKey(Business,on_delete=models.SET_NULL,null=True, blank=True)
    product_comment = models.ForeignKey(ProductComment,on_delete=models.SET_NULL, null=True,blank=True)
    business_comment = models.ForeignKey(BusinessComment,on_delete=models.SET_NULL, null=True,blank=True)
    CHOICES = (
        ('PR','Product'),
        ('BUS','Business'),
        ('PRC','Product_comment'),
        ('BUSC','Business_comment'),    
    )
    notification_type = models.CharField(max_length=100,choices=CHOICES)


    def __str__(self):
        return self.text +'('+str(self.id)+')'


