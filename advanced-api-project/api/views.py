from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter
from django_filters import rest_framework

class BookListView(generics.ListAPIView):
    """
    Read-only list of books with filtering, searching, and ordering.

    Filters (via DjangoFilterBackend):
      - title: exact / icontains / istartswith
      - author: exact (author id)
      - author__name: icontains
      - publication_year: exact / gte / lte
      - year_min, year_max: friendly aliases for pub year range

    Search (via SearchFilter):
      - ?search=<text> matches title and author name (icontains)

    Ordering (via OrderingFilter):
      - ?ordering=publication_year  or  ?ordering=-publication_year
      - multiple: ?ordering=publication_year,-title
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ["title", "author__name"]
    ordering_fields = ["id", "title", "publication_year", "author__name"]
    ordering = ["id"]
