# Generated by Django 4.2 on 2024-12-20 12:39

import accounts.models
import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='photo',
            field=models.ImageField(blank=True, storage=accounts.models.OverwriteStorage(), upload_to=accounts.utils.rename_imagefile_to_uid),
        ),
    ]
