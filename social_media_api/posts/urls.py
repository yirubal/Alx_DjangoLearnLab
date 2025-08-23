# posts/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from posts.views import PostViewSet, CommentViewSet, FeedView

# Correct: Define router ONCE
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# Correct: Use that same router for nesting
posts_router = NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
]

# Add router URLs
urlpatterns += router.urls + posts_router.urls
