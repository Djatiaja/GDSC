# Generated by Django 5.0.1 on 2024-01-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hsk',
            name='link_academy',
            field=models.TextField(default='/', max_length=10000),
        ),
        migrations.AddField(
            model_name='hsk',
            name='link_dig',
            field=models.TextField(default='/', max_length=10000),
        ),
        migrations.AddField(
            model_name='hsk',
            name='link_pandarin',
            field=models.TextField(default='/', max_length=10000),
        ),
        migrations.AlterField(
            model_name='hsk',
            name='link_audio',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='hsk',
            name='link_reading',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='hsk',
            name='link_vocab',
            field=models.TextField(max_length=10000),
        ),
    ]
