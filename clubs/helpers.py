from django.conf import settings
from django.shortcuts import redirect
import csv
import os

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def generate_favourite_ratings(book,user):
    current_directory = os.getcwd()
    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    isbn = book.isbn
    user_id = user
    with open(rating_path,'a+') as rating_file:
        csv_writer = csv.writer(rating_file,delimiter=";")
        csv_writer.writerow([f"{user_id}",f'{isbn}','8'])
