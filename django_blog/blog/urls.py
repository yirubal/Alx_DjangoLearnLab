# python
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import HomeView, ProfileView, RegisterView, PostListView, PostDetailView, PostCreateView, PostUpdateView, \
    PostDeleteView

app_name = "blog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # Auth
    path("login/",  auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),


    path("posts/", PostListView.as_view(), name="posts"),                 # list
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"), # detail


    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),


]