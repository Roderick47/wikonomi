from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from Business.models import Business
from QA.models import Question

class HowTo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="A brief overview of what this process covers")
    
    # Links
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='how_tos', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='how_tos', null=True, blank=True)
    
    # Integration with QA
    origin_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, related_name='how_tos')
    
    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='how_tos_created')
    last_editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='how_tos_edited')
    
    is_official = models.BooleanField(default=False, help_text="Marked by business owner as official documentation")
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    views_count = models.PositiveIntegerField(default=0)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-is_official', '-created_at']
        verbose_name = "How To"
        verbose_name_plural = "How To's"

    def __str__(self):
        return self.title

class HowToStep(models.Model):
    how_to = models.ForeignKey(HowTo, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(help_text="Detailed instructions for this step")
    image = models.ImageField(upload_to='howto_steps/', null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order}: {self.title or 'Step'}"

class HowToHistory(models.Model):
    how_to = models.ForeignKey(HowTo, on_delete=models.CASCADE, related_name='history')
    version = models.PositiveIntegerField()
    editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    change_summary = models.CharField(max_length=255, blank=True, help_text="Optional description of what changed")
    
    # Store steps as JSON for a point-in-time snapshot without complex related models
    # This stores title, content, and image URL
    steps_snapshot = models.JSONField(default=list)

    class Meta:
        ordering = ['-version']
        verbose_name = "How To History"
        verbose_name_plural = "How To Histories"

    def __str__(self):
        return f"{self.how_to.title} - v{self.version}"
