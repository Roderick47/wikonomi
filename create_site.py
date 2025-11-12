import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIKONOMI.settings')
django.setup()

from django.contrib.sites.models import Site

# Create the default site
Site.objects.get_or_create(
    id=1,
    defaults={
        'domain': 'example.com',
        'name': 'example.com'
    }
) 