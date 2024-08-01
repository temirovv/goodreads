from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (
    Model, CharField, TextField, ForeignKey,
    EmailField, CASCADE, IntegerField, ImageField
)


class Book(Model):
    title = CharField(max_length=255)
    description = TextField()
    isbn = CharField(max_length=17)
    cover_picture = ImageField(default='default_cover_pic.jpg')

    def __str__(self):
        return self.title


class Author(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = EmailField()
    bio = TextField()

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(Model):
    book = ForeignKey('books.Book', CASCADE)
    author = ForeignKey('books.Author', CASCADE)

    def __str__(self):
        return f"{self.book.title} by {self.author.full_name}"


class BookReview(Model):
    user = ForeignKey(CustomUser, CASCADE)
    book = ForeignKey('books.Book', CASCADE)
    comment = TextField()
    stars_given = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.stars_given} by {self.user.last_name} {self.user.last_name}"
