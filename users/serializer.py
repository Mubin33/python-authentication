from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
User = get_user_model()

#  get active login user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email']



class LoginSerializer(serializers.Serializer):
    email =serializers.EmailField()
    password = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret
    

    
# for authentication (register user)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = { 'password': {'write_only': True}}

    # jodi nicer 3 line code 1tab shamne niye jai tahole ei def ta classs er under e cole jabe, and password encript hoye jabe
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
 