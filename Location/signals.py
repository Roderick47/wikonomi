from django.db.models.signals import post_save
from django.dispatch import receiver
from Product.models import Product

@receiver(post_save, sender=Product)
def update_product_location(sender, instance, created, **kwargs):
    if created:  # Only update location if the product is newly created
        # You can perform any additional logic here if needed
        instance.save()
