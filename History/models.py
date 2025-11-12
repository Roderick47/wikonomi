from django.db import models
from django.utils import timezone
from Product.models import Product

# Create your models here.

class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=300, blank=True)
    previous_author = models.CharField(max_length=100, null=True, blank=True)
    current_author = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    business = models.CharField(max_length=100, blank=True)
    is_public = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Ensure we have a creation date for new records
        if not self.pk:
            self.date_created = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def price_change(self):
        """Returns the price change between the last two history records"""
        allPH = ProductHistory.objects.filter(product=self.product).order_by('-id')
        allPHcount = allPH.count()
        if allPHcount < 2:
            return '-'
        else:
            lastPH = allPH[0]
            seclastPH = allPH[1]
            if lastPH.price is not None and seclastPH.price is not None:
                priceChange = lastPH.price - seclastPH.price 
                return priceChange
            return '-'

    def get_last_price(self):
        """Returns the last price from history, or current product price if no history"""
        last_history = ProductHistory.objects.filter(product=self.product).order_by('-id').first()
        if last_history and last_history.price is not None:
            return last_history.price
        elif self.product and self.product.price is not None:
            return self.product.price
        return None



