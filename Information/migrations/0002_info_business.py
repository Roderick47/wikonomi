# Generated by Django 5.0.2 on 2024-03-12 04:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Business', '0002_alter_business_description_alter_business_location'),
        ('Information', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Business.business'),
        ),
    ]
