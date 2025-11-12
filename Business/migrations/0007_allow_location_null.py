# Generated manually to allow NULL in location field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0006_clear_location_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ] 