from django.shortcuts import render

from .models import Book, BookInstance, Author, Genre


def index(request):
    """View function for home page of site"""

    total_number_of_books = Book.objects.count()
    total_number_of_book_instance = Book.objects.count()

    total_number_of_available_books = BookInstance.objects.filter(
        status__exact='a').count()

    total_number_of_authors = Author.objects.count()

    total_number_of_genre = Genre.objects.filter(name__contains='sci').count()

    context = {
        'total_number_of_books': total_number_of_books,
        'total_number_of_book_instance': total_number_of_books,
        'total_number_of_available_books': total_number_of_books,
        'total_number_of_authors': total_number_of_books,
        'total_number_of_genre': total_number_of_genre
    }

    return render(request, 'index.html', context=context)
