from relationship_app.models import Author, Library

# --- 1. Query all books by a specific author ---
author_name = "George Orwell"  # You can change this
author = Author.objects.get(name=author_name)
books_by_author = author.books.all()
print(f"Books by {author_name}:", [book.title for book in books_by_author])

# --- 2. List all books in a specific library ---
library_name = "City Library"  # Change this to test another library
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print(f"Books in {library_name}:", [book.title for book in books_in_library])

# --- 3. Retrieve the librarian for a library ---
librarian = library.librarian  # Uses related_name from OneToOneField
print(f"Librarian for {library_name}:", librarian.name)

