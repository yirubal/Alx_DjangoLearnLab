from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # Columns in admin list
    list_filter = ('publication_year', 'author')             # Right-side filters
    search_fields = ('title', 'author')                      # Search box
from django.contrib import admin

# Register your models here.
