from django.db.models.signals import post_save
from django.dispatch import receiver
from Product.models import Product
from History.models import ProductHistory


@receiver(post_save,sender=Product)
def ProductHistoryOnCreate(sender,created,instance,**kwargs):
    if created:
        ph = ProductHistory()
        ph.business = instance.business
        ph.product = instance
        ph.name = instance.name
        ph.price = instance.price
        if ph.current_author: ph.current_author = instance.author.username
        ph.description = instance.description
        ph.date_created = instance.date_created
        ph.date_updated = instance.date_updated
        ph.is_public = instance.is_public
        ph.save()



# Signal that creates a 'backup' or saves a History of the Product. This is called after the product is edited.
@receiver(post_save,sender=Product)
def ProductHistoryOnEdit(sender,created,instance,**kwargs):
    if not created:
        ph = ProductHistory()
        ph.business = instance.business
        ph.product = instance
        ph.price = instance.price
        ph.name = instance.name
        ph.description = instance.description
        ph.previous_author = ProductHistory.objects.filter(product=instance).order_by('id').last().current_author
        ph.current_author = instance.author.username
        ph.date_created = instance.date_created
        ph.date_updated = instance.date_updated
        ph.is_public = instance.is_public
        ph.save()



