from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, BookInstance, Author, Genre


def index(request):
    """View function for home page of site"""

    total_number_of_books = Book.objects.count()
    total_number_of_book_instance = Book.objects.count()

    total_number_of_available_books = BookInstance.objects.filter(
        status__exact='a').count()

    total_number_of_authors = Author.objects.count()

    total_number_of_genre = Genre.objects.filter(name__contains='sci').count()

    number_of_visits = request.session.get('number_of_visits', 1)
    request.session['number_of_visits'] = number_of_visits + 1

    context = {
        'total_number_of_books': total_number_of_books,
        'total_number_of_book_instance': total_number_of_books,
        'total_number_of_available_books': total_number_of_books,
        'total_number_of_authors': total_number_of_books,
        'total_number_of_genre': total_number_of_genre,
        'number_of_visits': number_of_visits
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter()[:5]


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUser(LoginRequiredMixin, generic.ListView):

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
