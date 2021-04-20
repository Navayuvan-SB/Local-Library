from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

import datetime

from .models import Book, BookInstance, Author, Genre, Publisher
from catalog.forms import RenewBookForm

from .filters import BookFilter


def index(request):

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUser(LoginRequiredMixin, generic.ListView):

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksForLibrarian(PermissionRequiredMixin, generic.ListView):

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():

            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed'))

    else:

        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(
            initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):

    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {
        'date_of_death': '11/06/2020'
    }


class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'add-book'


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10


class GenreDetailView(generic.DetailView):
    model = Genre


class GenreCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'catalog.add_genre'
    model = Genre
    fields = ('name',)


class GenreUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'catalog.update_genre'
    model = Genre
    fields = ('name',)


class GenreDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'catalog.delete_genre'
    model = Genre

    success_url = reverse_lazy('genres')


class PublisherListView(generic.ListView):
    model = Publisher
    paginate_by = 10


class PublisherDetailView(generic.DetailView):
    model = Publisher


class PublisherCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'catalog.add_publisher'
    model = Publisher
    fields = ('name',)


class PublisherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'catalog.update_publisher'
    model = Publisher
    fields = ('name',)


class PublisherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'catalog.delete_publisher'
    model = Publisher

    success_url = reverse_lazy('publishers')
