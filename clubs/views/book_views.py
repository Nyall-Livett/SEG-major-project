"""User related views."""
import csv, io
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.list import MultipleObjectMixin
from clubs.models import Book, BooksRead
from clubs.content_based_recommender.content_based_recommend import content_based_recommender
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from clubs.forms import UploadBooksForm, BookForm, BookReviewForm
from django.views.generic.detail import DetailView
from ..helpers import generate_ratings
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

class BookListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""

    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = settings.BOOKS_PER_PAGE

class BookReviewView(LoginRequiredMixin, FormView):
    """docstring for BookReviewView."""

    template_name = "book_review.html"
    form_class = BookReviewForm

    def form_valid(self, form):
        review = form.instance
        review.reviewer = self.request.user
        try:
            review.save()
            generate_ratings(review.book,review.reviewer.id,review.rating)
            return super().form_valid(form)
        except IntegrityError as e:
            return render(self.request, "book_review.html")

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse('book_review')

class UploadBooksView(LoginRequiredMixin, FormView):
    form_class = UploadBooksForm
    template_name = "upload_books.html"

    def form_valid(self, form):

        csv_file = self.request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(self.request, 'Please upload a csv file')
            return self.render()

        data = csv_file.read().decode('ISO-8859-1')
        io_string = io.StringIO(data)


        for book in csv.reader(io_string, delimiter = ';', quotechar='"'):
            if(book[0] != 'ISBN'):
                try:
                    try:
                        _, created = Book.objects.update_or_create(
                            isbn = book[0].strip('"'),
                            name = book[1].strip('"'),
                            author = book[2].strip('"'),
                            publication_year = book[3].strip('"'),
                            publisher = book[4].strip('"'),
                            image_url_s = book[5].strip('"'),
                            image_url_m = book[6].strip('"'),
                            image_url_l = book[7].strip('"'),
                            category = book[8].strip('"').strip("'[]"),
                            grouped_category = book[9].strip('"').strip("'[]"),
                            description = book[10].strip('"')
                        )
                    except IndexError:
                        _, created = Book.objects.update_or_create(
                            isbn = book[0].strip('"'),
                            name = book[1].strip('"'),
                            author = book[2].strip('"'),
                            publication_year = book[3].strip('"'),
                            publisher = book[4].strip('"'),
                            image_url_s = book[5].strip('"'),
                            image_url_m = book[6].strip('"'),
                            image_url_l = book[7].strip('"'),
                        )
                except IndexError:
                    messages.add_message(self.request, messages.WARNING, f"{book[0]} could not be added to the system.")

        return super().form_valid(form)

    def render(self):
        """Render upload form with blank form."""
        form = UploadBooksForm()
        return render(self.request, 'upload_books.html', {'form': form})

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("book_list")

class ShowBookView(LoginRequiredMixin, DetailView):

    model = Book
    template_name = 'show_book.html'
    pk_url_kwarg = 'book_id'

    def get(self, request, *args, **kwargs):
        """Handle get request, and redirect to book_list if book_id is invalid."""

        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('book_list')

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context['reviews'] = BooksRead.objects.all()
        book = Book.objects.get(id=self.kwargs.get('book_id'))
        try:
            book_name = book.name
            get_recommended_books = content_based_recommender(book_name)
            books = []
            for i in get_recommended_books:
                book = Book.objects.filter(name=i).first()
                books.append(book)
            context['recommended_books'] = books
        except:
            context['recommended_books'] = None
        return context

class CreateBookView(LoginRequiredMixin, FormView):

    model = Book
    template_name = "set_book.html"
    form_class = BookForm


    def form_valid(self, form):
        book = form.instance
        book.save()
        return super().form_valid(form)

    def get(self, request):
        form2 = BookForm()
        context = {
            'form': form2
        }
        return render(request,"set_book.html", context)

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("book_list")


class AuthorBookListView(LoginRequiredMixin, ListView):
    """View that shows a list of all books of a specific author."""

    model = Book
    template_name = "books_by_author.html"
    paginate_by = settings.BOOKS_PER_PAGE


    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        book = Book.objects.get(id=self.kwargs.get('book_id'))
        context['author'] =  book.author
        return context

    def get_queryset(self):
        book = Book.objects.get(id=self.kwargs.get('book_id'))
        return Book.objects.filter(author=book.author)

class PublisherBookListView(LoginRequiredMixin, ListView):
    """View that shows a list of all books published by a specific publisher."""

    model = Book
    template_name = "books_by_publisher.html"
    paginate_by = settings.BOOKS_PER_PAGE


    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        book = Book.objects.get(id=self.kwargs.get('book_id'))
        book_publisher = book.publisher
        context['publisher'] = book_publisher
        return context

    def get_queryset(self):
        book = Book.objects.get(id=self.kwargs.get('book_id'))
        book_publisher = book.publisher
        return Book.objects.filter(publisher=book_publisher)
