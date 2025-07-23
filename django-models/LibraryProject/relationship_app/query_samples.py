from relationship_app.models import Author, Book, Library

# --- 1. Query all books by a specific author ---
author_name = "George Orwell"  # Change this if needed
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)  # ✅ matches expected check
print(f"Books by {author_name}:", [book.title for book in books_by_author])

# --- 2. List all books in a specific library ---
library_name = "City Library"  # Change this if needed
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()  # ManyToMany relation
print(f"Books in {library_name}:", [book.title for book in books_in_library])

# --- 3. Retrieve the librarian for a library ---
librarian = library.librarian  # ✅ OneToOne reverse lookup
print(f"Librarian for {library_name}:", librarian.name)


