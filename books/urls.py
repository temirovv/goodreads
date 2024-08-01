from django.urls import path
from .views import BookListView,BookDetailView


app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='books'),
    path('<int:id>/', BookDetailView.as_view(), name='detail')
]
