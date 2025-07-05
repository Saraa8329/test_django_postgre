from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = "myapp/book_list.html"

class BookDetailView(DetailView):
    model = Book
    template_name = "myapp/book_detail.html"

class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "published_date", "genre", "isbn"]
    template_name = "myapp/book_form.html"
    success_url = reverse_lazy("book-list")
