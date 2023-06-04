from rest_framework.views import APIView, Response
from .serializers import RecordSerializer, ReportSerializer
from .models import MedicalRecord, MedicalReport
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsPatient, IsMedic
from users.authentication import JSONWebTokenAuthentication
from users.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from django.http import HttpResponse
from users.custom_renderers import ImageRenderer


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

class CreateRecordView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    
    def post(self, request):
        data = dict(request.data)
        data['title'] = data['title'][0]
        data['image'] = data['image'][0]
        data['user'] = request.user.id
        print(data)
        serializer = RecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        print(serializer.errors)
        return Response(data=serializer.errors, status=500)
    
class RecordImageView(generics.RetrieveAPIView):
    renderers_classes = [ImageRenderer]
    def get(self, request, id):
        queryset = MedicalRecord.objects.get(id=id).image
        data = queryset
        return HttpResponse(data, content_type='image/' + data.path.split(".")[-1])