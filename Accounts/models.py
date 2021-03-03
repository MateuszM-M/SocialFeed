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
    lastname = models.CharField(max_length=50)
    gender = models.CharField(max_length=22, choices=GENDER, default='X', blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(default="profile.png", blank=True, upload_to='images/')
    motto = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ContactManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Contact.objects.filter(receiver=receiver, status='send')
        return qs


class Contact(models.Model):
    STATUS_CHOICES = (
        ('send', 'send'),
        ('accepted', 'accepted')
    )

    sender = models.ForeignKey(Profile,
                               on_delete=models.CASCADE,
                               related_name='sender')
    receiver = models.ForeignKey(Profile,
                                 on_delete=models.CASCADE,
                                 related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="send")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = ContactManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
