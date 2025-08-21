from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet, CommentViewSet
from rest_framework_nested.routers import NestedDefaultRouter
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# The lookup **must** be 'post' so DRF gives you kwargs['post_pk']
posts_router = NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = router.urls + posts_router.urls
# urlpatterns = [
#     # path('', PostListView.as_view(), name='post-list'),
#     # path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
#     # path('<int:post_id>/comments', CommentListView.as_view(), name='comment-list'),
#     # path('comments/<int:pk>', CommentDetailView.as_view(), name='comment-detail')
#
# ]

