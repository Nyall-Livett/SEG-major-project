from django.conf import settings
from django.shortcuts import redirect
import pandas as pd
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

def generate_ratings(book,user,review):
    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    isbn = book.isbn
    user_id = user
    if(review=="like"):
        rating = 8
    elif(review=="neutral"):
        rating = 5
    elif(review=="dislike"):
        rating = 2
    with open(rating_path,'a+') as rating_file:
        csv_writer = csv.writer(rating_file,delimiter=";")
        csv_writer.writerow([f"{user_id}",f'{isbn}',f'{rating}'])

def delete_ratings(user):
    rating_path = '/Users/wxy/Documents/SEG/SEG-major-project/clubs/book_database/BX-Book-Ratings_formatted.csv'
    ratings = pd.read_csv(rating_path,delimiter=";",header=0)
    ratings=ratings.rename({'User-ID': 'User_ID'},axis=1)
    ratings = ratings.drop(ratings.query(f'User_ID=={user}').index)
    ratings=ratings.rename({'User_ID': 'User-ID'},axis=1)
    ratings.to_csv(rating_path, index=False,sep = ';')
