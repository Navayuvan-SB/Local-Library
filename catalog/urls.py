from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index")
]

urlpatterns += [
    path('books/', views.BookListView.as_view(), name="books"),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name="book-detail"),
    path('book/<int:pk>/update/',
         views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/',
         views.BookDelete.as_view(), name='book-delete'),
]

urlpatterns += [
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>',
         views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/<int:pk>/update/',
         views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/',
         views.AuthorDelete.as_view(), name='author-delete'),
]


urlpatterns += [
    path('genres/',
         views.GenreListView.as_view(), name='genres'),
    path('genre/<int:pk>',
         views.GenreDetailView.as_view(), name='genre-detail'),
    path('genre/create/',
         views.GenreCreateView.as_view(), name='genre-create'),
    path('genre/<int:pk>/edit',
         views.GenreUpdateView.as_view(), name='genre-update'),
    path('genre/<int:pk>/delete',
         views.GenreDeleteView.as_view(), name='genre-delete'),
]


urlpatterns += [
    path('publishers/',
         views.PublisherListView.as_view(), name='publishers'),
    path('publisher/<int:pk>',
         views.PublisherDetailView.as_view(), name='publisher-detail'),
    path('publisher/create/',
         views.PublisherCreateView.as_view(), name='publisher-create'),
]


urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,
         name='renew-book-librarian'),
    path('mybooks/', views.LoanedBooksByUser.as_view(), name="my-borrowed"),
    path('borrowed/', views.BorrowedBooksForLibrarian.as_view(), name="borrowed"),
]
