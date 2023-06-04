from rest_framework.decorators import APIView
from rest_framework.views import Response
from .models import Demand, Task
from .serializers import DemandSerializer, TaskSerializer, TaskDemandSerializer, DemandCoordsSerializer
from users.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsDriver
from users.serializers import ProfileSerializer, UserSerializer
from users.models import User

class MyDemandView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] # add worker + patients here
    def get(self, request):
        objects = Demand.objects.filter(state='A', user=request.user)
        serializer = DemandSerializer(objects, many=True)
        for demand in serializer.data:
            if demand['creator'] != None:
                creator = User.objects.filter(id=demand['creator']).first()
                demand['creator'] = f'{creator.email}'
            demand['user'] = User.objects.filter(id=demand['user']).first().email
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
        
    # def put(self, request):
    #     id = request.data.get('id')
    #     if not id:
    #         return Response({'error': 'can\'t finish without id'})
        
    #     instance = Demand.objects.filter(id=id).first()
    #     if not instance:
    #         return Response({'error': 'there are no element with such id'})
    #     if (instance.user.id == request.user.id):
    #         if instance.state in ('A', 'T'):
    #             instance.state = 'F'
    #             # here cancel the tasks too
    #             instance.save()
    #             return Response({'id': id})
    #         else:
    #             return Response({'error': 'the demand is already canceld or finished'}) 
    #     else:
    #         return Response({'error': 'non authorized'})
        
class MyDemandOldView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] # add worker + patients here
    def get(self, request):
        objects = Demand.objects.filter(user=request.user).exclude(state='A')
        serializer = DemandSerializer(objects, many=True)
        for demand in serializer.data:
            if demand['creator'] != None:
                creator = User.objects.filter(id=demand['creator']).first()
                demand['creator'] = f'{creator.email}'
            demand['user'] = User.objects.filter(id=demand['user']).first().email
        return Response(serializer.data)

class OtheresDemandView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] # add worker + patients here
    def get(self, request):
        objects = Demand.objects.filter(creator=request.user)
        serializer = DemandSerializer(objects, many=True)
        for demand in serializer.data:
            if demand['creator'] != None:
                creator = User.objects.filter(id=demand['creator']).first()
                demand['creator'] = f'{creator.email}'
            demand['user'] = User.objects.filter(id=demand['user']).first().email
        return Response(serializer.data)

    def post(self, request):
        id = request.data.pop('id')
        if not id:
            return Response({'error': 'can\'t demand without id'}, status=401)
        data = request.data.copy()
        data['user'] = id
        data['creator'] = request.user.id
        serializer = DemandSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        return Response(DemandSerializer(instance).data)
    
class MyTaskView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
            tasks = Task.objects.filter(user=request.user, state='A')
            serializer = TaskSerializer(instance=tasks, many=True)
            data = [dict(**(TaskSerializer(task).data), longitude=task.demand.longitude, latitude=task.demand.latitude, patient=task.demand.user.id, patient_name=f'{task.demand.user.first_name} {task.demand.user.last_name}')for task in tasks]
            return Response(data)
    
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
    
class MyTaskOldView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
            tasks = Task.objects.filter(user=request.user).exclude(state='A')
            serializer = TaskSerializer(instance=tasks, many=True)
            data = [dict(**(TaskSerializer(task).data), longitude=task.demand.longitude, latitude=task.demand.latitude, patient=task.demand.user.id, patient_name=f'{task.demand.user.first_name} {task.demand.user.last_name}')for task in tasks]
            return Response(data)

class OnMeTaskView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
            tasks = Task.objects.filter(demand__user=request.user, state='A')
            serializer = TaskSerializer(instance=tasks, many=True)
            data = [dict(**(TaskSerializer(task).data), longitude=task.demand.longitude, latitude=task.demand.latitude, patient=task.user.id, patient_name=f'{task.user.first_name} {task.user.last_name}', turn=task.team.turn())for task in tasks]
            print(data)
            return Response(data)

class MyTeamMembersView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]
    def get(self, request):
        team = request.user.team
        if team:
            users = set()
            for tasks in team.task_set.all():
                if tasks.user:
                    users.add(tasks.user)
            data = []
            for user in users:
                user_data = UserSerializer(instance=user).data
                profile_data = ProfileSerializer(instance=user.profile).data
                profile_data.pop('id')
                profile_data.pop('user')
                data.append(dict(**(user_data), **(profile_data)))
            return Response(data=data, status=200)
        return Response(data={'error':'This user has no team.'}, status=400)
    
class MyTeamDirection(APIView):
    permission_classes = [IsAuthenticated, IsDriver]
    def get(self, request):
        team = request.user.team
        if team:
            coords = []
            for task in team.task_set.all().order_by('order'):
                coords.append(task.demand)
            serializer = DemandCoordsSerializer(instance=coords, many=True)
            print(serializer.data)
            return Response(data=serializer.data, status=200)
        return Response(data={'error':'This user has no team.'}, status=400)

class MyTeamInfoView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
            user = request.user
            if user.profile.type == 'Driver':
                pass