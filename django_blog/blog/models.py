from django.conf import settings
from django.db import models

class Post(models.Model):
    """
    A single blog post written by one author (User).
    One author -> many posts (reverse: user.posts.all()).
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,     # delete posts if user is deleted
        related_name="posts",         # enables user.posts.all()
    )

    def __str__(self) -> str:
        return self.title
