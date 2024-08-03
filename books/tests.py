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

    def test_search_books(self):
        book1 = Book.objects.create(title='Sport', description='Description1', isbn='111111')
        book2 = Book.objects.create(title='History', description='Description2', isbn='222222')
        book3 = Book.objects.create(title='True', description='Description3', isbn='333333')

        response = self.client.get(reverse('books:books') + '?q=sport')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:books') + '?q=history')
        self.assertNotContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:books') + '?q=true')
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertContains(response, book3.title)



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

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'abc')
        self.assertContains(response, 'abcdescription')
        self.assertContains(response, '11111111')
