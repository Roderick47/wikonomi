from django.db import models
from Product.models import Product
from Business.models import Business    
from django.db.models.signals import post_save
from django.db.models import Avg, Max, Min

from django.dispatch import receiver

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product,blank=True,related_name='tags')
    businesses = models.ManyToManyField(Business,blank=True)

    def __str__(self):
        return self.name

    def cheapest(self):
        return self.products.aggregate(Min('price'))
    
    def average(self):
        return self.products.aggregate(Avg('price'))
    
    def maximum(self):
        return self.products.aggregate(Max('price'))
    

    

@receiver(post_save,sender=Product)
def create_product_tag(sender,instance,created,**kwargs):
    if created:
        try: 
            tag = Tag.objects.get(name=instance.name)
        except Tag.DoesNotExist:
            tag = Tag(name=instance.name)
            tag.save()
        tag.products.add(instance)
        tag.save()





# @register.filter(name="isCheapest")
# def isCheapest(product):
#     label = ''
#     for tag in product.tag_set.all():
#         lowest_price = tag.products.aggregate(Min('price'))
#         average_price = tag.products.aggregate(Avg('price'))
#         highest_price = tag.products.aggregate(Max('price'))
#         if product.price < 0.8*int(average_price['price__avg']):
#             label = "cheap"
#         if product.price == lowest_price['price__min']:
#             label = "cheapest-price"
#         if product.price >= 1.3*int(average_price['price__avg']):
#             label = "expensive"
#         if product.price == highest_price['price__max']:
#             label = "most-expensive"
#     return label
