from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from .models import Book


class BookListView(ListView):
    template_name = 'books/book-list.html'
    queryset = Book.objects.all()
    context_object_name = 'books'

# class BookListView(View):
#     def get(self, request):
#         books = Book.objects.all()
#
#         return render(request, 'books/book-list.html', context={'books': books})


class BookDetailView(DetailView):
    template_name = 'books/book-detail.html'
    pk_url_kwarg = 'id'
    model = Book
    context_object_name = 'book'


# class BookDetailView(View):
#     def get(self, request, id):
#         book = Book.objects.filter(id=id).first()
#         return render(request, 'books/book-detail.html', context={'book': book})
