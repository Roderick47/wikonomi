from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from Business.models import Business

def get_image_filename(instance,filename):
    slug=slugify(str(instance.user.username+'/profile.png'))
    return slug



# Profile for each users
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,blank=True)

    def __str__(self):
        return self.user.username+'['+str(self.id) +']'

    def has_business(self):
        try:
            b =  Business.objects.filter(author=self.user)
            return (True,b)
        except Business.DoesNotExist:
            return False


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
