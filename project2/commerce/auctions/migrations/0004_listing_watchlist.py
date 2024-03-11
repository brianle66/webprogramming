# Generated by Django 5.0.3 on 2024-03-09 14:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchList',
            field=models.ManyToManyField(blank=True, null=True, related_name='userwatchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]