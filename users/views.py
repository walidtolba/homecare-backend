from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import HttpResponse
from django.conf import settings
from rest_framework import parsers, renderers, status
from .serializers import AuthTokenSerializer
from .serializers import UserSerializer, UserCreationSerializer, ProfileSerializer, ProfilePictureSerializer, UserVerificationRecordSerializer
import jwt, datetime
from .models import User, VerificationCode
import random
from django.core.mail import send_mail
from .custom_renderers import JPEGRenderer
from rest_framework import generics


class ImageAPIView(generics.RetrieveAPIView):
    renderers_classes = [JPEGRenderer]
    def get(self, request, id):
        queryset = User.objects.get(id=id).profile.picture
        data = queryset
        return HttpResponse(data, content_type='image/jpg')

class Image2APIView(generics.RetrieveAPIView):
    renderers_classes = [JPEGRenderer]
    def get(self, request, id):
        queryset = User.objects.get(id=id).profile.picture
        data = queryset
        return HttpResponse(data, content_type='image/png')

class JSONWebTokenAuth(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = jwt.encode({
                'email': serializer.validated_data['email'],
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)
            }, settings.SECRET_KEY, algorithm='HS256')
            return Response({'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SignupView(APIView): 
    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        code = ''.join([str(random.choice(range(10))) for i in range(5)])
        verificationCode = VerificationCode(code=code, user=instance)
        verificationCode.save()
        data = serializer.validated_data
        subject = 'welcome to HomeCare'
        message = f'Hi {data["first_name"]} {data["last_name"]} , thank you for registering in HomeCare, your verification code is: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = (data['email'],)
        send_mail( subject, message, email_from, recipient_list )
        return Response({'email': data['email']})

class SignupVerificationView(APIView): # Not complete
    def post(self, request):
        code = request.data['code'] 
        user = User.objects.filter(email=request.data['email']).first()
        user_code = VerificationCode.objects.filter(user=user.id).first()   
        if code == user_code.code:
            user_code.delete()
            user.is_active = True
            user.save()
            return Response({'email': user.email})
        return Response({'error': 'Can\'t verify user'})
    
class ProfileView(APIView):
    def post(self, request):
        #debanage:
        data = request.data.copy()
        email = data.pop('email')
        if (email):
            data['user'] = User.objects.filter(email=email).first().id

        # end
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        data = serializer.validated_data.copy()
        data['user'] = data['user'].email
        return Response(data)
    
# I used this
class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_data = UserSerializer(instance=user).data
        profile_data = ProfileSerializer(instance=user.profile).data
        profile_data.pop('id')
        profile_data.pop('user')
        data = dict(**(user_data), **(profile_data))
        return Response(data=data)
    
class OtherProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        user_data = UserSerializer(instance=user).data
        profile_data = ProfileSerializer(instance=user.profile).data
        profile_data.pop('id')
        profile_data.pop('user')
        data = dict(**(user_data), **(profile_data))
        return Response(data=data)
    
# I used this 
class CareAboutMeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = request.user.profile.caregivers
        users_data = UserSerializer(instance=users, many=True).data
        return Response(data=users_data)
    def post(self, request):
        email = request.data.pop('email')
        if email:
            user = User.objects.filter(email=email).first()
            if (user):
                request.user.profile.caregivers.add(user)
                users = request.user.profile.caregivers
                users_data = UserSerializer(instance=users, many=True).data
                return Response(data=users_data)
            return Response({'error': 'Invalid Email'}, status=400)

        return Response({'error': 'Please provide the Caregiver email'}, status=400)
    def delete(self, request):
        id = request.data.pop('id')
        if id:
            request.user.profile.caregivers.remove(id)
            users = request.user.profile.caregivers
            users_data = UserSerializer(instance=users, many=True).data
            return Response(data=users_data)
        

# I used this
class ICareAboutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = request.user.care_about
        users = [user.user for user in users.all()]
        users_data = UserSerializer(instance=users, many=True).data
        return Response(data=users_data)

class DeclareAbsance(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        profile = request.user.profile
        if not profile.is_absent:
            profile.is_absent = True
            profile.save()
            return Response({'id': request.user.id, 'is_absent': True})
        return Response({'error': 'You are already absent'}, status=401)
    
    def delete(self, request):
        profile = request.user.profile
        if profile.is_absent:
            profile.is_absent = False
            profile.save()
            return Response({'id': request.user.id, 'is_absent': True})
        return Response({'error': 'You are already present'}, status=401)

    
class ProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    
    def post(self, request):
        profile = request.user.profile
        serializer = ProfilePictureSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=500)
    
class UserVerificationRecord(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user
        serializer = UserVerificationRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=500)