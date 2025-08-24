# from rest_framework import serializers
# from posts.models import Post, Comment
#
# class PostSerializer(serializers.ModelSerializer):
#     author_username = serializers.CharField(source="author.username", read_only=True)
#
#     class Meta:
#         model = Post
#         fields = ["id", "title", "content", "author_username", "created_at"]
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('id', 'content',  'created_at')
#         model = Comment




from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user", "liked_at"]
        read_only_fields = ["id", "user", "liked_at"]


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "content", "author_username", "created_at")


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author_username", "created_at", "like_count", "is_liked"]

    def get_like_count(self, obj):
        # No related_name on Like.post → use default reverse manager: like_set
        return obj.like_set.count()

    def get_is_liked(self, obj):
        req = self.context.get("request")
        if not req or not req.user.is_authenticated:
            return False
        return obj.like_set.filter(user=req.user).exists()
