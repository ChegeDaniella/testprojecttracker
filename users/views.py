from django.shortcuts import render
from .forms import UserLoginForm
from .models import Users
from .serializers import UserLoginSerializer,UsersSerializer
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.conf import settings 
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password

class UserLoginView(APIView):
    # import pdb; pdb.set_trace()
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer


    def post(self, request):
        # import pdb; pdb.set_trace() 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message' : 'User logged in successfully',
            'token' :serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)   

class UsersList(APIView):
    def get (self, request, format=None):
        all_users = Users.objects.all()
        serializers = UsersSerializer(all_users ,many=True) 
        return Response(serializers.data)     

# @login_required
class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    #giving permission to authenticated user
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)
    
    #permission
    def logout(self, request):
        # import pdb; pdb.set_trace()
        token = request.user.auth_token
        if request.user.is_authenticated():

            print(token)
            try:
                request.user.auth_token.delete()
            except (AttributeError, ObjectDoesNotExist):
                pass


        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response




