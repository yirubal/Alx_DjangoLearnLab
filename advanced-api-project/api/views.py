from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    Read-only list of books with simple filtering:
      - ?search=<text> (title contains, case-insensitive)
      - ?author_id=<id>
      - ?year=<yyyy>
      - ?year_min=<yyyy>&year_max=<yyyy>
      - ?ordering=publication_year or -publication_year
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["publication_year", "title", "id"]
    ordering = ["id"]

    def get_queryset(self):
        qs = Book.objects.select_related("author").all()

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search)

        author_id = self.request.query_params.get("author_id")
        if author_id:
            qs = qs.filter(author_id=author_id)

        year = self.request.query_params.get("year")
        if year:
            qs = qs.filter(publication_year=year)

        ymin = self.request.query_params.get("year_min")
        ymax = self.request.query_params.get("year_max")
        if ymin:
            qs = qs.filter(publication_year__gte=ymin)
        if ymax:
            qs = qs.filter(publication_year__lte=ymax)

        return qs


class BookDetailView(generics.RetrieveAPIView):
    """Read-only detail of a single book."""
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    Requires authentication.
    Customizes validation behavior via perform_create.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Example hook: you could enforce additional business rules here.
        # The serializer already blocks future years.
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book (PUT/PATCH).
    Requires authentication.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Extra checks could go here (e.g., forbid author changes).
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
