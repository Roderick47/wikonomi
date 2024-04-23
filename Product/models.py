from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils import timezone
from django.urls import reverse
from Business.models import get_image_filename,Business
from Location.models import Location    
#from Follow.models import ProductSubscription

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=300,blank=True)
    # image = models.ForeignKey(Photo,on_delete=models.SET_NULL,null=True)
    business  = models.ForeignKey(Business,on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_public = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name +' ['+'K ' +str(self.price)+']'
    
    def FirstPhoto(self):   
        return self.productphoto_set.first()
    
    def AllPhotos(self):
        return self.productphoto_set.all()

    def get_absolute_url(self):
        return reverse("Product:detail", kwargs={"prod_id": self.pk})

    def is_followed(self,request):
        subscription = request.user.productsubscription_set.get(product=self.product)
        if subscription.exist():
            return True
        else: 
            return False 
        

    def price_change(self):
        from History.models import ProductHistory
        allPH = ProductHistory.objects.filter(product=self).order_by('-id')
        if allPH.count() > 1:
            change = allPH[1].price - allPH[0].price
            return change
        else:
         return False


    # def is_recent_update(self):
    #     return  self.date_updated.date >= datetime.now() - timedelta(days=1)

