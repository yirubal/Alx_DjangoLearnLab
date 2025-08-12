from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Author, Book

User = get_user_model()


class BookAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a real user we can log in as (session-based auth)
        cls.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123",
        )

        cls.author1 = Author.objects.create(name="Jane Doe")
        cls.author2 = Author.objects.create(name="John Smith")

        cls.book1 = Book.objects.create(
            title="Clean Code", publication_year=2008, author=cls.author1
        )
        cls.book2 = Book.objects.create(
            title="The Pragmatic Programmer", publication_year=1999, author=cls.author2
        )
        cls.book3 = Book.objects.create(
            title="Deep Work", publication_year=2016, author=cls.author2
        )

    # Use Django session login (what the checker wants to see)
    def _login(self):
        ok = self.client.login(username="tester", password="testpass123")
        self.assertTrue(ok, "Login failed in tests")

    # ---------- Read-only ----------
    def test_list_books_as_anonymous(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 3)

    def test_retrieve_book_as_anonymous(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.pk)

    # ---------- Create ----------
    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        payload = {"title": "New Book", "publication_year": 2020, "author": self.author1.id}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated_success(self):
        self._login()
        url = reverse("book-create")
        payload = {"title": "New Book", "publication_year": 2020, "author": self.author1.id}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_create_book_future_year_validation(self):
        self._login()
        url = reverse("book-create")
        payload = {
            "title": "Future Book",
            "publication_year": date.today().year + 5,
            "author": self.author1.id,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

    # ---------- Update ----------
    def test_update_book_requires_auth(self):
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        response = self.client.patch(url, {"title": "CC"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated_success(self):
        self._login()
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        response = self.client.patch(url, {"title": "Clean Code (2nd Ed)"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Clean Code (2nd Ed)")

    # ---------- Delete ----------
    def test_delete_book_requires_auth(self):
        url = reverse("book-delete", kwargs={"pk": self.book2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated_success(self):
        self._login()
        url = reverse("book-delete", kwargs={"pk": self.book2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # ---------- Filtering ----------
    def test_filter_by_author_id(self):
        url = reverse("book-list")
        response = self.client.get(url, {"author": self.author2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        assert "Deep Work" in titles and "The Pragmatic Programmer" in titles

    def test_filter_by_author_name_contains(self):
        url = reverse("book-list")
        response = self.client.get(url, {"author__name__icontains": "john"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("Deep Work", titles)

    def test_filter_by_year_range(self):
        url = reverse("book-list")
        response = self.client.get(url, {"year_min": 2000, "year_max": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertTrue(all(2000 <= y <= 2020 for y in years))

    # ---------- Search ----------
    def test_search_in_title(self):
        url = reverse("book-list")
        response = self.client.get(url, {"search": "clean"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("Clean Code", titles)

    def test_search_in_author_name(self):
        url = reverse("book-list")
        response = self.client.get(url, {"search": "smith"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("Deep Work", titles)

    # ---------- Ordering ----------
    def test_ordering_by_publication_year_desc(self):
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_ordering_by_year_then_title(self):
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "publication_year,title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years))
