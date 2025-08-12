import django_filters as filters
from .models import Book

class BookFilter(filters.FilterSet):
    # Friendly aliases for ranges
    year_min = filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    year_max = filters.NumberFilter(field_name="publication_year", lookup_expr="lte")

    class Meta:
        model = Book
        # You may use complex lookups via double-underscore
        fields = {
            "title": ["exact", "icontains", "istartswith"],
            "publication_year": ["exact", "gte", "lte"],
            "author": ["exact"],            # by author id
            "author__name": ["icontains"],  # filter by author name
        }
