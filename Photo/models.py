from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from Product.models import Product
from Business.models import Business
from django.utils.text import slugify


def get_image_filename(instance,filename):
    slug = slugify(instance.product.name)
    fslug= slugify(filename)
    return 'products/{}/{}.jpg'.format(slug,fslug)

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_image_filename,null=True, blank=True)

    # def __str__(self):
    #     return self.photo.filename

class BusinessPhoto(models.Model):
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_image_filename,null=True, blank=True)

    def __str__(self):
        return str(self.business.name)



@receiver(post_delete, sender=ProductPhoto)
def submission_delete(sender,instance,**kwargs):
    if instance.photo:
        instance.photo.delete(False)

   