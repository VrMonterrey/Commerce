# Generated by Django 4.1.5 on 2023-02-24 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='desc',
            new_name='description',
        ),
    ]
