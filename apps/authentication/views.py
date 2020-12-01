from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.shortcuts import render
from django.core.mail import send_mail

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView, View
from rest_framework_simplejwt.views import TokenObtainPairView

from . import models
from .serializers import ChangePasswordSerializer
from apps.authentication.serializers import (
    RegisterApiSerializer, LoginSerializer, LogoutSerializer
)

User_ = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_mail('Ваш активационный код!', f"Активационный код: {user.activation_code}", 'smilestyle312@gmail.com', [user.email])
                return Response(
                 serializer.data, status=status.HTTP_201_CREATED
                )

class ActivationApiView(APIView):
    def get(self, request, activation_code):
        print(activation_code)
        try:
            user = User_.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({"message": "Successfully activated"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Noo"}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer

class Logout(APIView):
    serializer_class = LogoutSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


