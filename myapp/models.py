from django.db import models

# Create your models here.
class hsk(models.Model):
    judul = models.CharField(max_length = 100)
    deskripsi = models.TextField(max_length = 10000)
    link_audio = models.TextField(max_length = 1000)
    link_vocab = models.TextField(max_length = 1000)
    link_reading = models.TextField(max_length = 1000)