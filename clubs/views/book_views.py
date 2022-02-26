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
from clubs.forms import UploadBooksForm, BookForm
from django.views.generic.detail import DetailView
import json
from urllib.request import urlopen
import os

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




        for book in csv.reader(io_string, delimiter = ';', quotechar='"'):
            if(book[0] != 'ISBN'):
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

class Openfile():
    # print(os.getcwd())
    # current_path = os.path.dirname(__file__)
    # print(current_path)
    # new_path = os.path.relpath('..\\book_database\\bigger_test.csv', os.getcwd())
    # print(new_path)
    # print(os.getcwd() + "/book_database/bigger_test.csv")


    #
    # current_path = os.path.dirname(__file__)
    #
    # new_path = os.path.relpath('..\\book_database\\bigger_test.csv', current_path)
    # with open(new_path, 'r') as f:
    #     reader = csv.reader(csvinput)
    #
    #     row = next(reader)
    #     print(row)

    # with open(os.getcwd() + "/clubs/book_database/bigger_test.csv",'r') as csvinput:
    #     with open(os.getcwd() + "/clubs/book_database/books_with_categories.csv", 'w') as csvoutput:
    #         writer = csv.writer(csvoutput, lineterminator='\n',  delimiter=";", quotechar='"')
    #         reader = csv.reader(csvinput)
    #
    #         all = []
    #         row = next(reader)
    #         row.append('\"Category\"')
    #         all.append(row)
    #
    #         for row in reader:
    #             row.append("\"GDFSGREGERGV\"")
    #             all.append(row)
    #
    #         writer.writerows(all)

    def get_book_categories(row):

        isbn = row[0]
        api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

        api_response = urlopen(api + isbn)
        book_data = json.load(api_response)

        try:
            volume_info = book_data["items"][0]["volumeInfo"]

            try:
                categories =  volume_info['categories']
            except:
                categories = ""
        except:
            categories = ""

        return categories

    current_directory = os.getcwd()

    with open(current_directory + "/clubs/book_database/bigger_test.csv",'r') as csvfile:
        with open(current_directory + "/clubs/book_database/books_with_categories.csv", 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n',  delimiter=";", quoting=csv.QUOTE_ALL)
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')

            all = []
            row = next(reader)
            new_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'Category']

            all.append(new_row)

            for row in reader:
                categories = get_book_categories(row)
                new_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], categories]
                all.append(new_row)

            writer.writerows(all)

#
#
# class GetBookView():
#     while True:
#
#         # create getting started variables
#         api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
#         isbn = input("Enter 10 digit ISBN: ").strip()
#
#         # send a request and get a JSON response
#         resp = urlopen(api + isbn)
#         # parse JSON into Python as a dictionary
#         book_data = json.load(resp)
#
#         # create additional variables for easy querying
#         volume_info = book_data["items"][0]["volumeInfo"]
#         author = volume_info["authors"]
#         # practice with conditional expressions!
#         prettify_author = author if len(author) > 1 else author[0]
#
#         # display title, author, page count, publication date
#         # fstrings require Python 3.6 or higher
#         # \n adds a new line for easier reading
#
#         print(book_data)
#         print(book_data["items"][0]["searchInfo"])
#
#
#         print(f"\nTitle: {volume_info['title']}")
#         print(f"Author: {prettify_author}")
#         print(f"Page Count: {volume_info['pageCount']}")
#         print(f"Publication Date: {volume_info['publishedDate']}")
#         print("\n***\n")
#         try:
#             categories = volume_info['categories']
#             print(f"\nCategories: {categories}")
#         except:
#             print("This book has no saved categories")
#
#         try:
#             main_categories = volume_info['mainCategory']
#             print(f"\nCategories: {main_categories}")
#         except:
#             print("This book has no saved main categories")
#
#         # ask user if they would like to enter another isbn
#         user_update = input("Would you like to enter another ISBN? y or n ").lower().strip()
#
#         if user_update != "y":
#             print("May the Zen of Python be with you. Have a nice day!")
#             break # as the name suggests, the break statement breaks out of the while loop
