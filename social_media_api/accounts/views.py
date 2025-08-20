from contextvars import Token

from django.contrib.auth import authenticate
from requests import Response
# Create your views here.
from rest_framework import generics

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser
from accounts.serializers import UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
    

class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
             taken = Token.objects.get(user=user)
             return Response({'token': taken.key})
        else:
            return Response({'error': 'Invalid Credentials'})


class UserProfileView(generics.RetrieveUpdateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

