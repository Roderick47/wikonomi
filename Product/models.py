from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
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
    date_updated = models.DateTimeField(default=timezone.now, editable=False)
    location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True)

    def save(self, *args, **kwargs):
        # Update date_updated to current time
        self.date_updated = timezone.now()
        # Call the parent class's save method
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} [K {self.price}]"
    
    def FirstPhoto(self):   
        return self.productphoto_set.first()
    
    def AllPhotos(self):
        return self.productphoto_set.all()

    def get_absolute_url(self):
        return reverse("Product:detail", kwargs={"prod_id": self.pk})

    def is_followed(self,request):
        subscription = request.user.productsubscription_set.filter(product=self).first()
        if subscription:
            return True
        else: 
            return False 
        

    def get_last_price(self):
        """Returns the previous price from history (not the current price)"""
        from History.models import ProductHistory
        # Get the second most recent history entry (skip the first one which is the current price)
        last_history = ProductHistory.objects.filter(product=self).order_by('-id')[1:2].first()
        if last_history and last_history.price is not None:
            return last_history.price
        return self.price  # Fallback to current price if no history

    def get_last_price_date(self):
        """Returns the date of the previous price change"""
        from History.models import ProductHistory
        # Get the second most recent history entry
        last_history = ProductHistory.objects.filter(product=self).order_by('-id')[1:2].first()
        if last_history:
            return last_history.date_created
        return None
        
    def has_price_history(self):
        """Check if there is any price history (at least one previous price)"""
        from History.models import ProductHistory
        Print('Cars')

        print('Product History Count: ', ProductHistory.objects.filter(product=self).count())
        result = ProductHistory.objects.filter(product=self).count()
        return result

    def get_price_history_stats(self):
        """Returns a dict with price change stats if applicable"""
        from History.models import ProductHistory
        history = ProductHistory.objects.filter(product=self).order_by('-id')[:2]
        
        if len(history) < 2:
            return None
            
        current = history[0].price
        previous = history[1].price
        
        if current is None or previous is None:
            return None
            
        difference = current - previous
        if difference == 0:
            return None
            
        percentage = (difference / previous * 100) if previous != 0 else 0
        
        return {
            'current': current,
            'previous': previous,
            'difference': difference,
            'percentage': abs(percentage),
            'is_increase': difference > 0,
            'is_decrease': difference < 0
        }

    def has_price_history(self):
        """Returns True if the product has any price history beyond the initial creation"""
        from History.models import ProductHistory
        return ProductHistory.objects.filter(product=self).count() > 1


    # def is_recent_update(self):
    #     return  self.date_updated.date >= datetime.now() - timedelta(days=1)

