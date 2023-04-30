from django.db import models

class SupportMessage(models.Model):
    types = (('L', 'Login Problem'), ('S', 'Sign up Problem'), ('N', 'No Type'))
    email = models.EmailField()
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    isAnswred = models.BooleanField(default=False)
    answer = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=types, default='N')

    def __str__(self):
        return self.email