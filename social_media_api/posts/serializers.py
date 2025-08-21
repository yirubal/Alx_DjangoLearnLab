from rest_framework import serializers
from posts.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author_username", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'content',  'created_at')
        model = Comment