# Generated manually to set location to NULL

from django.db import migrations


def set_location_null(apps, schema_editor):
    """Set location field to NULL instead of empty string"""
    Business = apps.get_model('Business', 'Business')
    
    # Set location to NULL for all businesses
    Business.objects.update(location=None)


def reverse_set_location_null(apps, schema_editor):
    """Reverse the NULL setting if needed"""
    Business = apps.get_model('Business', 'Business')
    
    # Set location back to empty string
    Business.objects.update(location='')


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0007_allow_location_null'),
    ]

    operations = [
        migrations.RunPython(set_location_null, reverse_set_location_null),
    ] 