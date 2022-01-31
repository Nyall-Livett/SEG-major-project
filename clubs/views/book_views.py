"""User related views."""
import csv, io
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.list import MultipleObjectMixin
from clubs.models import Book
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from clubs.forms import UploadBooksForm

class BookListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""

    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = settings.BOOKS_PER_PAGE

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
        next(io_string)

        for book in csv.reader(io_string, delimiter = ';', quotechar='"'):
            try:
                _, created = Book.objects.update_or_create(
                    isbn = book[0].strip('"'),
                    name = book[1].strip('"'),
                    author = book[2].strip('"'),
                    publication_year = book[3].strip('"'),
                    publisher = book[4].strip('"'),
                    image_url_s = book[5].strip('"'),
                    image_url_m = book[6].strip('"'),
                    image_url_l = book[7].strip('"')
                )
            except ValueError:
                messages.add_message(self.request, messages.WARNING, f"{self.book.name} could not be added to the system.")

        return super().form_valid(form)

    def render(self):
        """Render upload form with blank form."""
        form = UploadBooksForm()
        return render(self.request, 'upload_books.html', {'form': form})

    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse("book_list")