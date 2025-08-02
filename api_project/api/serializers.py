from rest_framework import serializers
from .models import Book  # Assuming you have a Book model

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
