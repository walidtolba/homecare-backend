from rest_framework import serializers
from .models import Demand, Task, Absance
from rest_framework.exceptions import ValidationError

class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    
    def validate_demand(self, demand):
        if demand.state != 'A':
            raise ValidationError('Demand must be active')
        return demand

class AbsanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absance
        fields = '__all__'
    
    def validate(self, attrs):
        if attrs['firstDate'] > attrs['lastDate']:
            raise ValidationError('first date must come before last date')
        return super().validate(attrs)