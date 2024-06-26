# Generated by Django 5.0.2 on 2024-03-10 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_alter_product_date_created_and_more'),
        ('Tag', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='tags', to='Product.product'),
        ),
    ]
