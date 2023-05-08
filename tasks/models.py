from django.db import models
from users.models import User

class Demand(models.Model):
    types = (('M', 'Medic'), ('N', 'Nurse'), ('D', 'Driver'))
    states = (('A', 'Active'), ('F', 'Finished'), ('C', 'Canceld'))

    type = models.CharField(max_length=3, choices=types)
    description = models.TextField(blank=True)
    willaia = models.CharField(max_length=64)
    daira = models.CharField(max_length=64)
    baladia = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    home = models.CharField(max_length=64)
    state = models.CharField(max_length=1, choices=states, default='A')
    isUrgent = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'demand id {self.id} by {self.user.email}'

class Task(models.Model):
    states = (('A', 'Active'),('T', 'Tasked'), ('F', 'Finished'), ('C', 'Canceled'))

    date = models.DateTimeField()
    description = models.TextField(blank=True)
    willaia = models.CharField(max_length=64)
    daira = models.CharField(max_length=64)
    baladia = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    home = models.CharField(max_length=64)
    state = models.CharField(max_length=1, choices=states, default='A')
    creation_date = models.DateTimeField(auto_now_add=True)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_me')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f'task id {self.id} for demand id {self.demand.id} by {self.user.email}'
    
class Absance(models.Model):
    states = (('A', 'Active'), ('C', 'Canceld'))

    firstDate = models.DateTimeField()
    lastDate = models.DateTimeField(blank=True, null=True)
    canUrgence = models.BooleanField(default=True)
    state = models.CharField(max_length=1, choices=states, default='A')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'absance id {self.id} for {self.user.email}'
