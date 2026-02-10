from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BugReport(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bug_reports', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Please describe the bug in detail.")
    expected_behavior = models.TextField(blank=True, help_text="What did you expect to happen?")
    url_route = models.CharField(max_length=200, blank=True, help_text="The page URL where the bug occurred")
    screenshot = models.ImageField(upload_to='bug_reports/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
