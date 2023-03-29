from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    genders = (('F', 'Female'), ('M', 'Male'))
    bloodTypes = (('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'))
    civilStatus = (('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced'))
    
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    birthDate = models.DateField()
    gender = models.CharField(max_length=1, choices=genders)
    bloodType = models.CharField(max_length=3, choices=bloodTypes)
    address = models.CharField(max_length=255)
    registeringDate = models.DateTimeField(auto_now_add=True)
    lastSeen = models.DateTimeField()
    isOnline = models.BooleanField()
    isActive = models.BooleanField()
    isVerified = models.BooleanField()
    picture = models.ImageField()
    civilStatus = models.CharField(max_length=1, choices=civilStatus)
    bio = models.TextField()
    isPublic = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)