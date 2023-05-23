from django.contrib import admin
from .models import MedicalRecord, MedicalReport

admin.site.register(MedicalReport)
admin.site.register(MedicalRecord)