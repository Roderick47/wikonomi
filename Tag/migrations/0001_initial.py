# Generated by Django 5.0.2 on 2024-02-10 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Business', '0001_initial'),
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('businesses', models.ManyToManyField(blank=True, to='Business.business')),
                ('products', models.ManyToManyField(blank=True, to='Product.product')),
            ],
        ),
    ]
