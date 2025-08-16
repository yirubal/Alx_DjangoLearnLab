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

    # Posts
    path("posts/", PostListView.as_view(), name="posts"),                 # list
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"), # detail
    path('posts/new', PostCreateView.as_view(), name='post-form'), #new
    path('posts/<int:pk>/edit', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),


]