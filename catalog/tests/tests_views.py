from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from catalog.models import Author, Genre, Language, Book, BookInstance

import datetime


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Christian {author_id}',
                last_name=f'Surname {author_id}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 10)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['author_list']) == 3)


class LoanedBookInstanceByUserListViewTest(TestCase):

    def setUp(self):

        # Create Users
        test_user1 = User.objects.create_user(
            username="testuser1", password="password1")
        test_user2 = User.objects.create_user(
            username="testuser2", password="password2")

        test_user1.save()
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(
            first_name="John", last_name="Mathews")
        test_genre = Genre.objects.create(name='fantasy')
        test_language = Language.objects.create(name="English")
        test_book = Book.objects.create(
            title="Book title",
            summary="Book summary",
            isbn="194873498",
            author=test_author,
            language=test_language
        )

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()

        # Create book instances
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):

            return_date = timezone.localtime() + datetime.timedelta(days=book_copy % 5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint='Unlikely Imprint, 260',
                due_back=return_date,
                borrower=the_borrower,
                status=status
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(
            response, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="password1")
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'catalog/bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_the_list(self):
        login = self.client.login(username="testuser1", password="password1")
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)

        books = BookInstance.objects.all()[:10]
        for book in books:
            book.status = 'o'
            book.save()

        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)

        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual('o', bookitem.status)

    def test_pages_ordered_by_due_date(self):

        for book in BookInstance.objects.all():
            book.status = 'o'
            book.save()

        login = self.client.login(username='testuser1', password='password1')
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0
        for book in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = book.due_back

            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back
