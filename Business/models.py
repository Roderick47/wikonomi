from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.text import slugify
from Location.models import Location

def get_image_filename(instance,filename):
    slug = slugify(instance.name)
    return slug

class Business(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    location_description = models.CharField(max_length=200, blank=True, help_text="Verbose description of the business location")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, help_text="GPS coordinates and address")
    image = models.ImageField(upload_to=get_image_filename,null=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name+' ['+str(self.pk)+']'

    def get_coordinates(self):
        """Return coordinates as a tuple if location exists and has coordinates"""
        if self.location and self.location.latitude is not None and self.location.longitude is not None:
            return (self.location.latitude, self.location.longitude)
        return None

    def has_gps_location(self):
        """Check if business has GPS coordinates"""
        return self.location is not None and self.location.latitude is not None and self.location.longitude is not None

