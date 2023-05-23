from rest_framework.views import APIView, Response
from .serializers import RecordSerializer, ReportSerializer
from .models import MedicalRecord, MedicalReport
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsPatient, IsMedic
from users.authentication import JSONWebTokenAuthentication
from users.models import User


class MyRecords(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self, request):
        records = MedicalRecord.objects.filter(user=request.user)
        serializer = RecordSerializer(instance=records, many=True)
        return Response(data=serializer.data)

    def delete(self, request):
        id = request.data.get('id')
        print(id)
        if not id:
            return Response({'error': 'can\'t delete without id'})
        instance = MedicalRecord.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.user.id == request.user.id):
            instance.delete()
            return Response({'id': id})
        else:
            return Response({'error': 'non authorized'})
        

class MyReports(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self, request):
        reports = MedicalReport.objects.filter(to=request.user)
        serializer = ReportSerializer(instance=reports, many=True)
        for report in serializer.data:
            report['email'] = User.objects.filter(id=report['by']).first().email
        return Response(data=serializer.data)

    def delete(self, request):
        id = request.data.get('id')
        print(id)
        if not id:
            return Response({'error': 'can\'t delete without id'})
        instance = MedicalReport.objects.filter(id=id).first()
        if not instance:
            return Response({'error': 'there are no element with such id'})
        if (instance.to.id == request.user.id):
            instance.delete()
            return Response({'id': id})
        else:
            return Response({'error': 'non authorized'})
        
class OthersRecords(APIView):
    permission_classes = [IsAuthenticated, IsMedic]
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self, request, id):
        records = MedicalRecord.objects.filter(user=id)
        serializer = RecordSerializer(instance=records, many=True)
        return Response(data=serializer.data)

class OthersReports(APIView):
    permission_classes = [IsAuthenticated, IsMedic]
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self, request, id):
        reports = MedicalReport.objects.filter(to=id)
        serializer = ReportSerializer(instance=reports, many=True)
        for report in serializer.data:
            report['email'] = User.objects.filter(id=report['by']).first().email
        return Response(data=serializer.data)

class OthersReportsCreate(APIView):
    permission_classes = [IsAuthenticated, IsMedic]
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self, request):
        data = request.data.copy()
        data['by'] = request.user.id
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response({'error': 'Invalid Date'}, status=401)