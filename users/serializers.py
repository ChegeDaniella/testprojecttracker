from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from .models import Users
from django.contrib.auth.hashers import make_password

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):


    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=130, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data):
        # import pdb; pdb.set_trace()
        email = data.get("email", None)
        raw_password = data.get("password", None)
        password = make_password(raw_password)
        
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
            'credentials not found')
        try:
            # import pdb; pdb.set_trace()

            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except Users.DoesNotExist:
            raise serializers.ValidationError(
            'user with this credentials does not exist')

        return {
            'email':user.email,
            'token' : jwt_token
        } 

class UsersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Users
        fields =('username','password')           



