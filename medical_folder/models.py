from django.db import models
from users.models import User

class MedicalReport(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    by = models.ForeignKey(on_delete=models.CASCADE, to=User, related_name='created_reports')
    to = models.ForeignKey(on_delete=models.CASCADE, to=User)

    def __str__(self):
        return self.title

class MedicalRecord(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField()
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(on_delete=models.CASCADE, to=User)

    def __str__(self):
        return self.title