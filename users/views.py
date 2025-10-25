from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializer import *
from .models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from knox.models import AuthToken
from rest_framework import status

User = get_user_model()
# Create your views here.

 

class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']


            user = authenticate(request, email=email, password=password)

            if user:
                _, token=AuthToken.objects.create(user)
                return Response(
                    {
                        "user": self.serializer_class(user).data,
                        "token": token
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error":"Invalid creadentials"}, status=401)

        else:
            return Response(serializer.errors, status=400)




class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        




# eta all user er list
class UserViewset(viewsets.ViewSet):
    # IsAuthenticated er kaygay jodi AllowAny hoy tahole token ba login chara jekono user data gulo access korte parbe 
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data) 