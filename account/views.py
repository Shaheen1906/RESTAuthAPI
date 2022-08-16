import email
from logging import raiseExceptions
from multiprocessing import context
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# generate tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
# Create your views here.
class UserRegistrationView(APIView):
    def post(self,request, format = None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response ({'token':token,'message':'Registration Successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self,request, format = None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response ({'token':token,'message':'Login Successfully'},status=status.HTTP_200_OK)
            else:
                return Response ({'errors':{'non_field_errors':['Email and password is no valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, format = None):
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response ({'message':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    def post(self,request, format = None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response ({'message':'Reset Link.please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    def post(self,request, uid, token, format = None):
        serializer = UserPasswordResetSerializer(data=request.data, context = {'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response ({'message':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)