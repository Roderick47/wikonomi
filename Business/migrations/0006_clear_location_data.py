# Generated manually to clear old location data

from django.db import migrations


def clear_old_location_data(apps, schema_editor):
    """Clear the old location field data before converting to ForeignKey"""
    Business = apps.get_model('Business', 'Business')
    
    # Clear the old location field data
    Business.objects.update(location='')


def reverse_clear_old_location_data(apps, schema_editor):
    """Reverse the data clearing if needed"""
    Business = apps.get_model('Business', 'Business')
    
    # Restore location_description to location field
    for business in Business.objects.all():
        if business.location_description:
            business.location = business.location_description
            business.save()


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0005_copy_location_data'),
    ]

    operations = [
        migrations.RunPython(clear_old_location_data, reverse_clear_old_location_data),
    ] 