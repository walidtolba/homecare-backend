from rest_framework import serializers
from .models import SupportMessage
from rest_framework.exceptions import ValidationError

class CreateSupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = ['title', 'email', 'content']