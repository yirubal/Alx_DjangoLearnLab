from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserLogoutView, UnfollowUser, FollowUser

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('follow/<int:pk>/', FollowUser.as_view(), name='follow'),
    path('unfollow/<int:pk>/', UnfollowUser.as_view(), name='unfollow')

]