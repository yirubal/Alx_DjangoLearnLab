from django.shortcuts import render

# Create your views here.
from .models import Book
from .forms import  SearchForm
from .forms import SearchForm

def search_books(request):
    form = SearchForm(request.GET)
    books = Book.objects.none()
    if form.is_valid():
        title = form.cleaned_data['title']
        books = Book.objects.filter(title__icontains=title)
    return render(request, 'bookshelf/book_list.html', {'books': books, 'form': form})
# Using Django ORM to prevent SQL injection





