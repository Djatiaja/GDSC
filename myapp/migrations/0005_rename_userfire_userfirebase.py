# Generated by Django 5.0.1 on 2024-02-16 10:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_userfire'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='userFire',
            new_name='userFirebase',
        ),
    ]
