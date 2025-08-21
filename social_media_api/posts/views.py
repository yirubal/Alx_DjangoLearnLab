from django.core.exceptions import ValidationError
from rest_framework import generics, filters

from posts.permissions import  IsAuthorOrReadOnly
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.



class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']  # Fields to search in

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListView(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['content']  # Filtering based on comment content

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            raise ValidationError("The post you're trying to comment on does not exist.")

        serializer.save(author=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


