from django.db import models

class SupportMessage(models.Model):
    email = models.EmailField()
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email