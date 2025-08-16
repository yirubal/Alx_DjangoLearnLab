
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("content", "author__username", "post__title")