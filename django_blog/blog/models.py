from django.conf import settings
from django.db import models
from django.contrib.auth.models import User




class Post(models.Model):
    """
    A single blog post written by one author (User).
    One author -> many posts (reverse: user.posts.all()).
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,     # delete posts if user is deleted
        related_name="posts",         # enables user.posts.all()
    )

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"