from django.db import models
from django.urls import reverse


# Create your models here.
class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return "location: {}, {}".format(self.latitude, self.longitude)
    
    def get_absolute_url(self):
        return reverse('Location:location',kwargs={'pk':self.pk})
    
