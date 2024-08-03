from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.core.paginator import Paginator

from .models import Book


# class BookListView(ListView):
#     template_name = 'books/book-list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by =


class BookListView(View):
    def get(self, request):
        books = Book.objects.order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 1)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(
            request,
            'books/book-list.html',
            context={'page_obj': page_obj, 'search_query': search_query})


class BookDetailView(DetailView):
    template_name = 'books/book-detail.html'
    pk_url_kwarg = 'id'
    model = Book
    context_object_name = 'book'


# class BookDetailView(View):
#     def get(self, request, id):
#         book = Book.objects.filter(id=id).first()
#         return render(request, 'books/book-detail.html', context={'book': book})
