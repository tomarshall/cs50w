# Generated by Django 5.0.7 on 2024-07-30 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
