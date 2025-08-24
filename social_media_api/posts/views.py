from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from rest_framework import filters, viewsets, generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from notifications.models import Notification
from posts.permissions import  IsAuthorOrReadOnly
from posts.models import Post, Comment, Like
from posts.serializers import PostSerializer, CommentSerializer, LikeSerializer
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
#  following_users = request.user.following.all()


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        # Get the list of users the current user is following
        if self.request.user.is_authenticated:
            following_users = self.request.user.following.all()
            return Post.objects.filter(author__in=following_users).order_by('-created_at')[:10]
        else:
            # Return an empty queryset for anonymous users
            return Post.objects.none()



class LikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer  # <-- add this

    def get(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'GET' not allowed. Use POST to toggle like."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.filter(post=post, user=request.user).delete()
            return Response({"message": f"You unliked the post '{post.title}'."}, status=status.HTTP_200_OK)
        else:
            Like.objects.create(post=post, user=request.user)
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target_content_type=ContentType.objects.get_for_model(Post),
                    target_object_id=post.id
                )
            return Response({"message": f"You liked the post '{post.title}'."}, status=status.HTTP_201_CREATED)








