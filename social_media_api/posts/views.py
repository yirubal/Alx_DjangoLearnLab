from django.core.exceptions import ValidationError
from rest_framework import  filters, viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.permissions import  IsAuthorOrReadOnly
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']  # Fields to search in

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthorOrReadOnly,)
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['content']  # Filtering based on comment content


    def get_queryset(self):
        qs = Comment.objects.all()

        # Support both nested routers and query param
        post_id = (
            self.kwargs.get("post_pk")
            or self.kwargs.get("post_id")
            or self.request.query_params.get("post")
        )
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs


    def perform_create(self, serializer):
        # Accept post from nested route or request data
        post_id = (
            self.kwargs.get("post_pk")
            or self.kwargs.get("post_id")
            or self.request.data.get("post")
        )
        if not post_id:
            raise ValidationError("A post_id is required to create a comment.")

        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

# class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthorOrReadOnly]
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


