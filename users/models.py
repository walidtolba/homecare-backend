from django.db import models
from django.contrib.auth.models import AbstractUser
from . import managers
import os

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')
    username = None
    is_support = models.BooleanField(default=False, help_text='Designates that this user can answer questions.', verbose_name='support status')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = managers.UserManager()

class Profile(models.Model):
    genders = (('F', 'Female'), ('M', 'Male'))
    bloodTypes = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'))
    types = [('Medic', 'Medic'), ('Nurse', 'Nurse'), ('Driver', 'Driver'), ('Patient', 'Patient')]
    def get_upload_to(self, filename):
        return os.path.join('images', 'profile_pictures', str(self.pk), filename)
    type = models.CharField(max_length=16, choices=types)
    title = models.CharField(max_length=64, null=True, blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=genders)
    blood_type = models.CharField(max_length=3, choices=bloodTypes)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_verified = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=get_upload_to, null=True, blank=True, default='images/profile_pictures/default_profile_picture.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    caregivers = models.ManyToManyField(User, null=True, blank=True, related_name='care_about')
    def __str__(self):
        return self.user.email


class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    creationDate = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email

class UserVerificationRecord(models.Model):
    def get_upload_to(self, filename):
        return os.path.join('images', 'profile_verification', str(self.user.pk), filename)
    type = models.CharField(max_length=64)
    image = models.ImageField(upload_to=get_upload_to)
    user = models.ForeignKey(on_delete=models.CASCADE, to=User)