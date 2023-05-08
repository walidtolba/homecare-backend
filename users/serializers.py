from rest_framework import serializers
from .models import User, VerificationCode, Profile, UserVerificationRecord

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class UserCreationSerializer(serializers.ModelSerializer): # There is a problem in this serializer
    cpassword = serializers.CharField(max_length=128)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'cpassword']
        extra_kawrgs = {
            'password': {'write_only': True},
            'cpassword2': {'write_only': True},
        }
    def validate(self, attrs):
        password = attrs.get('password')
        cpassword = attrs.get('cpassword')

        if not password or password != cpassword:
                raise serializers.ValidationError('Empty password or no not matched')
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        cpassword = validated_data.pop('cpassword', None)
        instance = self.Meta.model(**validated_data, is_active = False)
        instance.set_password(password)
        instance.save()
        return instance

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class VerificationCodeSerializer(serializers.ModelSerializer): # odn't need it
    class Meta:
        model = VerificationCode
        fields = ['code', 'user']
    
    def validate_code(self, value):
        if len(value) != 5:
            raise serializers.ValidationError('Verfication code length must be 5 numbers exactly')
        return value;

    def validate(self, attrs):
        code = attrs['code']
        user_code = VerificationCode.objects.filter(user=attrs['user'])
        if code != user_code:
            raise serializers.ValidationError('incorrect verification code')
        return super().validate(attrs)
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']
    
    def upload(self, instance, validated_data):
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance
    

class UserVerificationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']
    
    def create(self, validated_data):
        instance = UserVerificationRecord()
        instance.type = validated_data.get('type')
        instance.user = validated_data.get('user')
        if not validated_data.get('image'):
            pass #raise error here
        instance.image = validated_data.get('image')
        instance.save()
        return instance