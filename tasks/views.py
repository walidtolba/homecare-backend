from rest_framework.decorators import APIView
from rest_framework.views import Response
from .models import Demand, Task, Absance
from .serializers import DemandSerializer, TaskSerializer, TaskDemandSerializer, AbsanceSerializer
from users.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsPatient

class MyDemandView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Demand.objects.filter(state='A', user=request.user)
        serializer = DemandSerializer(objects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = DemandSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        return Response(DemandSerializer(instance).data)
    
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t delete without id'})
        
        instance = Demand.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.user.id == request.user.id):
            if instance.state == 'A':
                instance.state = 'C'
                # here cancel the tasks too
                instance.save()
                return Response({'id': id})
            else:
                return Response({'error': 'the demand is already canceld or finished'}) 
        else:
            return Response({'error': 'non authorized'})
        
    def put(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t finish without id'})
        
        instance = Demand.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.user.id == request.user.id):
            if instance.state == 'A':
                instance.state = 'F'
                # here cancel the tasks too
                instance.save()
                return Response({'id': id})
            else:
                return Response({'error': 'the demand is already canceld or finished'}) 
        else:
            return Response({'error': 'non authorized'})
        
class ListMyCanceledDemandView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Demand.objects.filter(state='C', user=request.user)
        serializer = DemandSerializer(objects, many=True)
        return Response(serializer.data)
    
class ListMyFinishedDemandView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Demand.objects.filter(state='F', user=request.user)
        serializer = DemandSerializer(objects, many=True)
        return Response(serializer.data)

class ByDemandMyTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='A', demand=request.data['demand'])
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.copy()
        data['to'] = request.user.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        return Response(TaskSerializer(instance).data)
    
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t delete without id'})
        
        instance = Task.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.to.id == request.to.id):
            if instance.state == 'A':
                instance.state = 'C'
                instance.save()
                return Response({'id': id})
            else:
                return Response({'error': 'the task is already canceld or finished or may be tasked'}) 
        else:
            return Response({'error': 'non authorized'})
        

class ListByDemandMyFinishedTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='F', demand=request.data['demand'], to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)

class ListByDemandMyCanceledTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='C', demand=request.data['demand'], to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)

class ListByDemandMyTaskedTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='T', demand=request.data['demand'], to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)
    
class ListMyActiveTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='A', to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)

class ListMyFinishedTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='F', to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)

class ListMyCanceledTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='C', to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)

class ListMyTaskedTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='T', to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)
    
class ByMeTasksView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, IsPatient]
    def get(self, request):
        objects = Task.objects.filter(state='A', to=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)
    
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t delete without id'})
        
        instance = Task.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.to.id == request.to.id):
            if instance.state == 'A':
                instance.state = 'C'
                instance.save()
                return Response({'id': id})
            else:
                return Response({'error': 'the task is already canceld or finished or may be tasked'}) 
        else:
            return Response({'error': 'non authorized'})


class MyTaskView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        state = request.data.get('state')
        if state in [state[0] for state in Task.states]:
            objects = Task.objects.filter(state=state, user=request.user)
        else:
            objects = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(objects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.dict()
        data['user'] = request.user.id
        serializer = TaskDemandSerializer(data=data)
        if serializer.is_valid():
            demand = Demand.objects.filter(id=request.data['demand']).first()
            demand.state = 'T'
            demand.save()
            instance = serializer.save()
            return Response(TaskSerializer(instance).data)
        return Response({'error': 'just for testing'})
    
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t delete without id'})
        instance = Task.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.user.id == request.user.id):
            if instance.state == 'A':
                demand = Demand.objects.filter(id=instance.demand.id).first()
                demand.state = 'A'
                instance.state = 'C'
                demand.save()
                instance.save()
                return Response({'canceled_task': id})
            else:
                return Response({'error': 'can\'nt cancel task'}) 
        else:
            return Response({'error': 'non authorized'})
        
    def put(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t finish task without id'})
        
        instance = Task.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.user.id == request.user.id):
            if instance.state == 'A':
                demand = Demand.objects.filter(id=instance.demand.id).first()
                demand.state = 'F'
                instance.state = 'F'
                demand.save()
                instance.save()
                return Response({'finished_task': id})
            else:
                return Response({'error': 'can\' finish task'}) 
        else:
            return Response({'error': 'non authorized'})
        

class MyAbsanceView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        objects = Absance.objects.filter(user=request.user)
        serializer = AbsanceSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.dict()
        data['user'] = request.user.id
        serializer = AbsanceSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(AbsanceSerializer(instance).data)
        return Response({'error': 'just for testing'})

    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t delete without id'})
        
        instance = Absance.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.user.id == request.user.id):
            if instance.state == 'A':
                instance.state = 'C'
                instance.save()
                return Response({'canceled_absance': id})
            else:
                return Response({'error': 'the absance is already canceld'}) 
        else:
            return Response({'error': 'non authorized'})
    
    def put(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'error': 'can\'t delete without id'})
        
        instance = Absance.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.user.id == request.user.id):
            if instance.state == 'C':
                instance.state = 'A'
                instance.save()
                return Response({'activated_absance': id})
            else:
                return Response({'error': 'the absance is already active'}) 
        else:
            return Response({'error': 'non authorized'})
