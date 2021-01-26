from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
        ('X', 'Do not want to specify'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50,)
    gender = models.CharField(max_length=22, choices=GENDER, default='X')
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(default="profile.png", blank=True, upload_to='images/')
    motto = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

