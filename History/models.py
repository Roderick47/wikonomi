from django.db import models
from Product.models import Product

# Create your models here.

class ProductHistory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,blank=True,default=product.name)
    description = models.TextField(max_length=300,blank=True,default=product.description)
    previous_author = models.CharField(max_length=100,null=True)
    current_author = models.CharField(max_length=100,null=True)
    price = models.FloatField(null=True)
    date_created = models.DateTimeField(null=True)
    date_updated = models.DateTimeField(null=True)
    business  = models.CharField(max_length=100,blank=True)
    is_public = models.BooleanField()

    def __str__(self):
        return self.name +' ('+str(self.id) + ')'

    def price_change(self):
        allPH = ProductHistory.objects.filter(product=self.product).order_by('-id')
        allPHcount = allPH.count()
        if allPHcount < 2:
            return '-'
        else:
            lastPH = allPH[0]
            seclastPH = allPH[1]
            priceChange = lastPH.price - seclastPH.price 
            return priceChange



