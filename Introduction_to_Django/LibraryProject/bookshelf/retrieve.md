
---

### 📄 `retrieve.md`

```markdown
# Retrieve the Book

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
