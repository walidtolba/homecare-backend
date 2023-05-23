from rest_framework import serializers
from .models import Demand, Task
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


class DemandCoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ['longitude', 'latitude']