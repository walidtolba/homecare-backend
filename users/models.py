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
    civilStatus = (('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced'))
    titles = [('M', 'Medic'), ('N', 'Nurse'), ('D', 'Driver'), ('F', 'Pharmasist'), ('P', 'Patient')]
    def get_upload_to(self, filename):
        return os.path.join('images', 'profile_pictures', str(self.pk), filename)
    title = models.CharField(max_length=1, choices=titles)
    birthDate = models.DateField()
    gender = models.CharField(max_length=1, choices=genders)
    bloodType = models.CharField(max_length=3, choices=bloodTypes)
    willaia = models.CharField(max_length=64)
    daira = models.CharField(max_length=64)
    baladia = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    home = models.CharField(max_length=64)
    job = models.CharField(max_length=128, null=True, blank=True)
    isOnline = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=get_upload_to, null=True, blank=True)
    civilStatus = models.CharField(max_length=1, choices=civilStatus)
    bio = models.TextField(blank=True, default='')
    isPublic = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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