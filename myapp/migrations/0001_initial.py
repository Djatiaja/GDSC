# Generated by Django 5.0.1 on 2024-01-12 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='hsk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=100)),
                ('deskripsi', models.TextField(max_length=10000)),
                ('link_audio', models.TextField(max_length=1000)),
                ('link_vocab', models.TextField(max_length=1000)),
                ('link_reading', models.TextField(max_length=1000)),
            ],
        ),
    ]
