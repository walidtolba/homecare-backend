from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser

from django.conf import settings

from rest_framework import parsers, renderers, status
from .serializers import AuthTokenSerializer

from .serializers import UserSerializer, UserCreationSerializer, VerificationCodeSerializer, ProfileSerializer, ProfilePictureSerializer, UserVerificationRecordSerializer

import jwt, datetime

from .models import User, VerificationCode

import random

from django.core.mail import send_mail

class LoginView(APIView): # Not used 
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Password incorrect')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'manel-helal', algorithm='HS256').encode('utf-8')

        return Response({'token': token})
    
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


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