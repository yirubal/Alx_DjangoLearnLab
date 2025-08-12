from datetime import date
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book. Adds validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        # You can also guard against unrealistic years if desired (e.g., < 1400)
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author with nested list of their books.
    - Uses the BookSerializer for the nested representation.
    - books is read-only here; you create books separately or implement a custom create().
    Relationship:
      Author (1) ---- (Many) Book via Book.author (related_name='books')
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
