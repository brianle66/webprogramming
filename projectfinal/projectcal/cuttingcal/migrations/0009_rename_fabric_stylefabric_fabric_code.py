# Generated by Django 5.0.6 on 2024-06-26 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuttingcal', '0008_remove_project_customer_remove_project_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stylefabric',
            old_name='fabric',
            new_name='fabric_code',
        ),
    ]