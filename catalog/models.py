from django.db import models


class Book(models.Model):
    """Model Representing a book (but not a specific copy of a book)"""

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of a book')

    isbn = models.CharField("ISBN", max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String representation for the model object"""
        return self.name

    def get_absolute_url(self):
        """Return the URL to access the details of this book"""
        return reverse("book_detail", args=[str(self.id)])


class Genre(models.Model):
    """Model Representing a book genre"""

    name = models.CharField(
        max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object"""

        return self.name
