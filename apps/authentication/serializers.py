from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from . import models
from django.contrib.auth.models import User
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import permissions

User_ = get_user_model()

class RegisterApiSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, 
        required=True, 
        write_only=True)
    password_confirmation = serializers.CharField(
        min_length=6, 
        required=True, 
        write_only=True
    )

    class Meta:
        model = User_
        fields = (
            'email', 
            'password', 
            'password_confirmation', 
            )

    def validate_email(self, value):
        if User_.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with given already exists!!!')
        return value 

    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError("Password don't match")
        return attrs


    def create(self, validated_data):
        user = User_.objects.create_user(**validated_data)
        return user



class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(
        min_length=6, write_only=True
        )

    def validate_email(self, value):
        if not User_.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with given email not found! Please resend with valid email')

        return value

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password', None)
        if not User_.objects.filter(email=email).exists():
            raise serializers.ValidationError('Not Found')

        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)

            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs

class LogoutSerializer(TokenObtainPairSerializer):
    permission_classes = permissions.IsAuthenticated

    def post(self, request):
        # django_logout(request)
        request.user.auth_token.delete()
        return Response(status=204)
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)