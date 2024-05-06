from django.db import models
from django.contrib.auth.models import User
from Business.models import Business

class Info(models.Model):
    type_choice = {'How to':'How to','Notice':'Notice',}
    type = models.CharField(max_length=100,choices=type_choice)
    name = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"Info: {{self.name}}"
