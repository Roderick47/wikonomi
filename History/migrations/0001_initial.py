# Generated by Django 5.0.2 on 2024-02-10 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=100)),
                ('description', models.TextField(blank=True, default='Foreign Key (type determined by related field)', max_length=300)),
                ('previous_author', models.CharField(max_length=100, null=True)),
                ('current_author', models.CharField(max_length=100, null=True)),
                ('price', models.FloatField(null=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('date_updated', models.DateTimeField(null=True)),
                ('business', models.CharField(blank=True, max_length=100)),
                ('is_public', models.BooleanField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product.product')),
            ],
        ),
    ]
