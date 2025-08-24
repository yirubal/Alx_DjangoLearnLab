from contextvars import Token

from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType
from requests import Response
# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser
from accounts.serializers import UserSerializer
from notifications.models import Notification
from posts.models import Post, Like


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # open endpoint (no token required)
    
    

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # open endpoint


    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
             taken, created = Token.objects.get_or_create(user=user)
             return Response({'token': taken.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=401)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]  # << crucial

    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            # Delete the user's token
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'




    def get_object(self):
        user_id = self.kwargs.get('pk')
        if int(user_id) != self.request.user.id:
            raise PermissionDenied("You do not have permission to access this profile.")
        return CustomUser.objects.get(pk=user_id)


class FollowUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = []

    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
        except CustomUser.MultipleObjectsReturned:
            return Response({"error": "Multiple users found"}, status=400)

        if request.user.pk == user_id:
            return Response({"error": "You cannot follow yourself."}, status=400)
        request.user.following.add(user)
        request.user.save()

        return Response({"message": "User followed successfully."})


class UnfollowUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]



    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
        except CustomUser.MultipleObjectsReturned:
            return Response({"error": "Multiple users found"}, status=400)

        if request.user.pk == user_id:
            return Response({"error": "You cannot unfollow yourself."}, status=400)

        request.user.following.remove(user)
        request.user.save()
        return Response({"message": "User unfollowed successfully."})


