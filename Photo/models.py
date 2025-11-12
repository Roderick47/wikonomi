from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from Product.models import Product
from Business.models import Business
from django.utils.text import slugify
from PIL import Image
import io

def get_image_filename(instance, filename):
    slug = slugify(instance.product.name)
    fslug = slugify(filename)
    return 'products/{}/{}.jpg'.format(slug, fslug)

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_image_filename, null=True, blank=True)

    def save(self, *args, **kwargs):
        # First save the model to ensure the file is properly saved
        super().save(*args, **kwargs)
        
        # Only process the image if it exists and has a path
        if self.photo and hasattr(self.photo, 'path') and self.photo.path:
            try:
                # Open the image using PIL
                img = Image.open(self.photo.path)
                
                # Convert to RGB mode if not already in that mode
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                # Set the maximum dimensions for the compressed image
                max_width = 1024
                max_height = 768
                
                # Check if the image needs to be resized
                if img.width > max_width or img.height > max_height:
                    # Resize the image while maintaining the aspect ratio
                    img.thumbnail((max_width, max_height))
                    
                    # Save the compressed image back to its original path
                    img.save(self.photo.path, quality=85, optimize=True)
            except Exception as e:
                # Log the error but don't fail the save
                print(f"Error processing image: {e}")

class BusinessPhoto(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_image_filename, null=True, blank=True)

    def __str__(self):
        return str(self.business.name)

    def save(self, *args, **kwargs):
        # First save the model to ensure the file is properly saved
        super().save(*args, **kwargs)
        
        # Only process the image if it exists and has a path
        if self.photo and hasattr(self.photo, 'path') and self.photo.path:
            try:
                # Open the image using PIL
                img = Image.open(self.photo.path)
                
                # Convert to RGB mode if not already in that mode
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                # Set the maximum dimensions for the compressed image
                max_width = 1024
                max_height = 768
                
                # Check if the image needs to be resized
                if img.width > max_width or img.height > max_height:
                    # Resize the image while maintaining the aspect ratio
                    img.thumbnail((max_width, max_height))
                    
                    # Save the compressed image back to its original path
                    img.save(self.photo.path, quality=85, optimize=True)
            except Exception as e:
                # Log the error but don't fail the save
                print(f"Error processing image: {e}")

@receiver(post_delete, sender=ProductPhoto)
def submission_delete(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(False)
