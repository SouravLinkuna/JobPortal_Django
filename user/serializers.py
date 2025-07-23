from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Method Name 'RecruiterSerialiser'
# Method Name 'UserSerialiser'
# Method Name 'AuthTokenSerializer' 

from rest_framework.authtoken.models import Token
from .models import UserDetails

class UserSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(min_length=4)
    # email = serializers.EmailField(
    #     validators=[UniqueValidator(queryset=UserDetails.objects.all(), message={'email': ['user details with this email already exists.']})],
    # )
    # mobile_number = serializers.IntegerField(
    #     validators=[UniqueValidator(queryset=UserDetails.objects.all(), message={'mobile_number': ['user details with this mobile number already exists.']})]
    # )
    # password = serializers.CharField()
    
    class Meta:
        model = UserDetails
        fields = ('name', 'email', 'designation', 'company', 'date_of_birth', 'gender', 'mobile_number', 'about_company', 'website', 'password')
        

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
