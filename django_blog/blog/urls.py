# python
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import HomeView, ProfileView, RegisterView

app_name = "blog"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    # Authentication
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Application
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),


]
