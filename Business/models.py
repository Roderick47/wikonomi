from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.text import slugify

def get_image_filename(instance,filename):
    slug = slugify(instance.name)
    return slug

class Business(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=get_image_filename,null=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name+' ['+str(self.pk)+']'

