# Generated by Django 5.0.1 on 2024-02-17 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_userfirebase_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hsk',
            name='link_writing',
            field=models.TextField(default='/', max_length=10000),
        ),
        migrations.AddField(
            model_name='hsk',
            name='link_writing2',
            field=models.TextField(default='/', max_length=10000),
        ),
        migrations.AddField(
            model_name='hsk',
            name='link_writing3',
            field=models.TextField(default='/', max_length=10000),
        ),
    ]
