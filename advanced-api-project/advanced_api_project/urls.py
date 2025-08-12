from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_index(_request):
    return JsonResponse({
        "project": "Advanced API Project",
        "endpoints": {
            "books_list": "/api/books/",
            "books_detail": "/api/books/<id>/",
            "books_create": "/api/books/create/",
            "books_update": "/api/books/<id>/update/",
            "books_delete": "/api/books/<id>/delete/",
        }
    })

urlpatterns = [
    path("", api_index, name="index"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # <— wire in the app urls
]
