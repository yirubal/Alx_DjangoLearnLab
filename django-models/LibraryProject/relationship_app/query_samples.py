from relationship_app.models import Author, Library

# 1. Query all books by a specific author
author = Author.objects.get(name="George Orwell")
books_by_author = author.books.all()
print("Books by George Orwell:", [book.title for book in books_by_author])

# 2. List all books in a library
library = Library.objects.get(name="City Library")
books_in_library = library.books.all()
print("Books in City Library:", [book.title for book in books_in_library])

# 3. Retrieve the librarian for a library
library = Library.objects.get(name="City Library")
librarian = library.librarian  # thanks to related_name in OneToOneField
print("Librarian for City Library:", librarian.name)
