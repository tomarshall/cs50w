# Generated by Django 5.0.7 on 2024-07-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=64),
        ),
    ]
