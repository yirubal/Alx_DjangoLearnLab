from django.urls import path, include
from posts.views import PostListView, PostDetailView, CommentListView, CommentDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comments', CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>', CommentDetailView.as_view(), name='comment-detail')
]

