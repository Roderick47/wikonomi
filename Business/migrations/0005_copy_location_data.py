# Generated manually to copy location data

from django.db import migrations


def copy_location_to_description(apps, schema_editor):
    """Copy existing location text to location_description"""
    Business = apps.get_model('Business', 'Business')
    
    for business in Business.objects.all():
        if business.location:
            business.location_description = business.location
            business.save()


def reverse_copy_location_to_description(apps, schema_editor):
    """Reverse the data migration if needed"""
    Business = apps.get_model('Business', 'Business')
    
    for business in Business.objects.all():
        if business.location_description:
            business.location = business.location_description
            business.save()


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0004_add_location_description_only'),
    ]

    operations = [
        migrations.RunPython(copy_location_to_description, reverse_copy_location_to_description),
    ] 