from django.db import models
from users.models import User

class MedicalReport(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    by = models.ForeignKey(on_delete=models.CASCADE, to=User)
    to = models.ForeignKey(on_delete=models.CASCADE, to=User)

class MedicalRecord(models.Model):
    image = models.ImageField()
    created_on = models.DateTimeField(auto_now_add=True)
    by = models.ForeignKey(on_delete=models.CASCADE, to=User, null=True)
    to = models.ForeignKey(on_delete=models.CASCADE, to=User)