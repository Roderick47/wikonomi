from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from Business.models import Business
from Information.models import Info

# Create your models here.


class ProductComment(models.Model):
    # sno = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    slug= models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,related_name="replies")

    def __str__(self):
        return self.user.username +": "+ self.body[:15]+"..."

    def has_reply(comment):
        if comment.parent:
            return True
        return False

    # def count_reply(comment):
    #     if 
    #     comment.parent
    def check_replies(self):
        if self.replies.exists():
            count=0
            for reply in self.replies.all():
                if reply.replies.exists():
                    count += reply.replies.count()
                else:
                    pass
                count += 1
            
            count += self.replies.count()
             
            if count:
                if count>1:
                    string = "[ {number} replies ]".format(number=count-1)
                if count == 1:
                    string = "[ {number} reply ]".format(number=count)
                return string
        else: 
            return ""

    def replies_count(self):
        if self.replies.count:

            return self.replies.count()


class BusinessComment(models.Model):
    business = models.ForeignKey(Business,on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    slug= models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,related_name="replies")

    def __str__(self):
        return self.user.username +": "+ self.body[:15]+"..."

    def has_reply(comment):
        if comment.parent:
            return True
        return False
    
    
class InfoComment(models.Model):
    info = models.ForeignKey(Info,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    slug= models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,related_name="replies")

    def __str__(self):
        return self.user.username +": "+ self.body[:15]+"..."

    def has_reply(comment):
        if comment.parent:
            return True
        return False
