from django.db import models

# Create your models here.

class Rate(models.Model):
    rate = models.FloatField()