from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class hsk(models.Model):
    judul = models.CharField(max_length = 100)
    deskripsi = models.TextField(max_length = 10000)
    link_audio = models.TextField(max_length = 10000, default='/')
    link_audio2 = models.TextField(max_length = 10000, default='/')
    link_audio3 = models.TextField(max_length = 10000, default='/')
    
    link_vocab = models.TextField(max_length = 10000)
    link_reading = models.TextField(max_length = 10000 , default='/')
    link_reading2 = models.TextField(max_length = 10000, default='/')
    link_reading3 = models.TextField(max_length = 10000, default='/')
    link_pandarin=models.TextField(max_length = 10000, default='/')
    link_academy=models.TextField(max_length = 10000, default='/')
    link_dig=models.TextField(max_length = 10000, default='/')

class user():
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
