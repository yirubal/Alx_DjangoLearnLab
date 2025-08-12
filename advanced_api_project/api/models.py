from django.db import models

# Create your models here.
from django.db import models

class Author(models.Model):
    """
    Author represents a single writer.
    - name: human-readable name of the author.
    One Author -> Many Books (reverse relation: author.books)
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """
    Book is written by exactly one Author.
    - title: book title
    - publication_year: integer year the book was published
    - author: FK to Author (one-to-many). related_name='books' gives Author.books
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",  # enables author.books
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
