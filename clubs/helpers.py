from django.conf import settings
from django.shortcuts import redirect
import pandas as pd
import csv
import os
import random
from .models import Book

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def generate_favourite_ratings(book,user):

    """When user signed up, generate rating for getting recommendations"""
    current_directory = os.getcwd()
    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    isbn = book.isbn
    user_id = user
    """Write rating to dataset file"""
    with open(rating_path,'a+') as rating_file:
        csv_writer = csv.writer(rating_file,delimiter=";")
        csv_writer.writerow([f"{user_id}",f'{isbn}','8'])
    """Drop repeated ratings"""
    drop_repeated_data()

def generate_ratings(book,user,review):

    """generate ratings when user add new book reads"""

    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    isbn = book.isbn
    user_id = user
    """According to the review, get rating value"""
    if(review=="like"):
        rating = 8
    elif(review=="neutral"):
        rating = 5
    elif(review=="dislike"):
        rating = 2
    """Write rating to dataset file"""
    with open(rating_path,'a+') as rating_file:
        csv_writer = csv.writer(rating_file,delimiter=";")
        csv_writer.writerow([f"{user_id}",f'{isbn}',f'{rating}'])
    """Drop repeated ratings"""
    drop_repeated_data()

def delete_ratings(user):

    """When user delete his/her account, delete the ratings they made"""
    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    ratings = pd.read_csv(rating_path,delimiter=";",header=0)
    """Change column name for easy data search"""
    ratings=ratings.rename({'User-ID': 'User_ID'},axis=1)
    ratings = ratings.drop(ratings.query(f'User_ID=={user}').index)
    ratings=ratings.rename({'User_ID': 'User-ID'},axis=1)
    ratings.to_csv(rating_path, index=False,sep = ';')

def contain_ratings(user):

    """Whether dataset has specific user rating or not"""
    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    ratings = pd.read_csv(rating_path,delimiter=";",header=0)
    ratings= ratings.rename({'User-ID': 'User_ID'},axis=1)
    ratings = ratings.query(f'User_ID=={user}')
    """Get the count of user ratings"""
    num = len(ratings)
    return (num>0)

def drop_repeated_data():
    """Drop repeated data"""
    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    ratings = pd.read_csv(rating_path,delimiter=";",header=0)
    ratings = ratings.drop_duplicates()
    ratings.to_csv(rating_path, index=False,sep = ';')

def get_ratings_count(user):
    """Get the count of specific user ratings"""
    rating_path = settings.BASE_DIR /'clubs/book_database/BX-Book-Ratings_formatted.csv'
    ratings = pd.read_csv(rating_path,delimiter=";",header=0)
    ratings= ratings.rename({'User-ID': 'User_ID'},axis=1)
    ratings = ratings.query(f'User_ID=={user}')
    counts = len(ratings)
    return counts
