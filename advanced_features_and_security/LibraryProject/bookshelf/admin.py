from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Book
from .models import CustomUser

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # Columns in admin list
    list_filter = ('publication_year', 'author')             # Right-side filters
    search_fields = ('title', 'author')                      # Search box
from django.contrib import admin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']
    search_fields = ['username', 'email']

admin.site.register(CustomUser, CustomUserAdmin)
