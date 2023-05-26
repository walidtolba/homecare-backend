from django.db import models
from users.models import User

class Demand(models.Model):
    types = (('Medic', 'Medic'), ('Nurse', 'Nurse'), ('Driver', 'Driver'))
    states = (('A', 'Active'), ('T', 'Tasked'), ('F', 'Finished'), ('C', 'Canceld'))

    type = models.CharField(max_length=16, choices=types)
    title = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=1, choices=states, default='A')
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=128, null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_demands')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'demand id {self.id} by {self.user.email}'
    
class Team(models.Model):

    turn = models.IntegerField(default=0)
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)


class Task(models.Model):
    states = (('A', 'Active'), ('F', 'Finished'), ('C', 'Canceled'))

    order = models.IntegerField()
    state = models.CharField(max_length=1, choices=states, default='A')
    creation_date = models.DateTimeField(auto_now_add=True)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


    def __str__(self):
        return f'task id {self.id} for demand id {self.demand.id}'


