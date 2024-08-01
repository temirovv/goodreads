from django.contrib.admin import register, ModelAdmin
from .models import Book, Author, BookAuthor, BookReview


@register(Book)
class BookAdmin(ModelAdmin):
    search_fields = ('title', 'description', 'isbn', )
    list_display = ('title', 'isbn', 'description', )


@register(Author)
class AuthorAdmin(ModelAdmin):
    pass


@register(BookAuthor)
class BookAuthorAdmin(ModelAdmin):
    pass


@register(BookReview)
class BookReviewAdmin(ModelAdmin):
    pass
