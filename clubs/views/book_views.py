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

# @login_required
# def get_recommended_books(request, book_id):
#     book_title = Book.objects.get(id=book_id).name

#     recommended_books = content_based_recommender(book_title)

#     return render(request, 'show_book.html', {'rec_books': recommended_books})


# class GetRecommendedBooks(LoginRequiredMixin, ListView):
#     model = Book
#     context_object_name = 'book_list'
#     paginate_by = settings.BOOKS_PER_PAGE

#     # def setup(self, request, book_id, *args, **kwargs):
#     #     super().setup(self, request, book_id, *args, **kwargs)
#     #     self.book_author = Book.objects.get(id=book_id).author

#     def get_queryset(self):
#         return Book.objects.filter(author='Stephen Fry')[:5]

#     def get_context_data(self, **kwargs):
#         context = super(GetRecommendedBooks, self).get_context_data(**kwargs)
#         context['book_list1'] = Book.objects.filter(author='Stephen Fry')[:5]
#         return context

@login_required
def get_books_by_author(request, book_id):
    book = Book.objects.get(id=book_id)
    book_name = book.name
    book_author = book.author

    filtered_by_author = Book.objects.filter(author=book_author).exclude(name=book_name)
    context = {'books_by_author': filtered_by_author}
    return render(request, 'books_by_author.html', context)

@login_required
def get_books_by_publisher(request, book_id):
    book = Book.objects.get(id=book_id)
    book_name = book.name
    book_publisher = book.publisher

    filtered_by_publisher = Book.objects.filter(author=book_publisher).exclude(name=book_name)
    context = {'books_by_publisher': filtered_by_publisher}
    return render(request, 'books_by_publisher.html', context)

@login_required
def get_recommended_books(request, book_id):
    book = Book.objects.get(id=book_id)
    book_name = book.name
    get_recommended_books = content_based_recommender(book_name)       #"Harry Potter and the Order of the Phoenix (Book 5)"
    recommended_books = []
    for i in get_recommended_books:
        book = Book.objects.filter(name=i).first()
            # print(book)

        recommended_books.append(book)
            # print(recommended_books)
    # except TypeError:
    #     print("Lalala")
    context = {'recommended_books': recommended_books}
    return render(request, 'recommended_books.html', context)
