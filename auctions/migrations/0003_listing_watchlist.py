# Generated by Django 4.1.5 on 2023-02-26 15:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_desc_listing_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchList',
            field=models.ManyToManyField(blank=True, null=True, related_name='ListingOwner', to=settings.AUTH_USER_MODEL),
        ),
    ]
