from django.test import TestCase
from django.urls import reverse
from .models import Book


class BookListTestcase(TestCase):
    def test_books_list_status_code(self):
        book = Book.objects.create(
            title='abc',
            description='abcdescription',
            isbn=11111111
        )
        book.save()

        response = self.client.get(
            path=reverse('books:books')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'abc')


class BookDetailTestCase(TestCase):
    def test_book_detail_exists(self):
        book = Book.objects.create(
            title='abc',
            description='abcdescription',
            isbn=11111111
        )
        book.save()

        response = self.client.get(
            path=reverse('books:detail', args=(1, ))
        )
        print(
            response.content
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'abc')
        self.assertContains(response, 'abcdescription')
        self.assertContains(response, '11111111')
