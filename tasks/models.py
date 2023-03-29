from django.db import models
from django.contrib.auth.models import User

class Demand(models.Model):
    types = (('M', 'Medic'), ('N', 'Nurse'), ('D', 'Driver'))
    states = (('A', 'Active'), ('T', 'Tasked'), ('F', 'Finished'), ('C', 'Canceld'))

    type = models.CharField(max_length=1, choices= types)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=1, choices=states, default='A')
    isUrgent = models.BooleanField(default=False)
    demandDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'demand number {self.id}'

class Task(models.Model):
    states = (('A', 'Active'), ('F', 'Finished'), ('C', 'Canceled'))

    date = models.DateTimeField()
    state = models.CharField(max_length=1, choices=states, default='A')
    creationDate = models.DateTimeField(auto_now_add=True)
    finishedDate = models.DateTimeField(blank=True, null=True)
    userRapport = models.TextField(blank=True, null=True)
    workerRapport = models.TextField(blank=True, null=True)
    isReported = models.BooleanField(default=False)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)

    def __str__(self):
        return f'task number {self.id} for the {str()}'
    
class Absance(models.Model):
  firstDate = models.DateTimeField()
  lastDate = models.DateTimeField(blank=True, null=True)
  canUrgence = models.BooleanField(default=True)
  worker = models.OneToOneField(User, on_delete=models.CASCADE)