import os
import csv
import sys
import re
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
import numpy as np
import json
from urllib.request import urlopen
from evaluator import Evaluator
import pandas as pd
import random

class ProcessData:

    isbn_to_title = {}
    title_to_isbn = {}
    current_directory = os.getcwd()
    ratingsPath = current_directory + '/BX-Book-Ratings_formatted.csv'
    booksPath = current_directory +  '/BX_Books_formatted.csv'
    preprocessedBooksPath = current_directory +  '/Preprocessed_Books_formatted.csv'


    def formatPreprocessedBooks(self):
        if not(os.path.exists(self.current_directory + '/Preprocessed_books_formatted.csv')):

            preprocessedData = pd.read_csv(self.current_directory + '/Preprocessed_data.csv', sep=',', encoding="latin-1", on_bad_lines='skip', quotechar = '"')

            preprocessedData.drop(columns = ['id', 'user_id', 'location','age', 'rating', 'city','state','country'],axis=1,inplace = True)
            preprocessedData=preprocessedData.reindex(columns= ['isbn', 'book_title', 'book_author', 'year_of_publication', 'publisher', 'img_s', 'img_m', 'img_l', 'Category', 'Summary', 'Language'])

            preprocessedData.rename(columns = {'isbn':'ISBN', 'book_title':'Book-Title', 'book_author':'Book-Author', 'year_of_publication':'Year-Of-Publication', 'publisher':'Publisher', 'img_s':'Image-URL-S', 'img_m':'Image-URL-M', 'img_l':'Image-URL-L'}, inplace=True)


            preprocessedData.drop_duplicates(subset='ISBN', keep='first', inplace=True, ignore_index=True)


            preprocessedData = preprocessedData.replace({'9': None})

            #Write all categories to a file called category.csv

            # categories = preprocessedData.Category.value_counts()
            # categories.to_csv(path_or_buf=self.current_directory + '/all_categories.csv')


            # Add the restricted category to the books


            mostPopularCategories = ["['Fiction']","['Juvenile Fiction']","['Biography & Autobiography']","['History']","['Juvenile Nonfiction']","['Social Science']","['Business & Economics']",
            "['Body, Mind & Spirit']","['Health & Fitness']","['Family & Relationships']","['Cooking']","['Humor']","['Computers']","['Psychology']","['Self-Help']","['Science']","['Travel']",
            "['Poetry']","['Literary Criticism']","['Art']","['Sports & Recreation']","['Philosophy']","['Nature']","['Political Science']","['Drama']","['Reference']","['Performing Arts']",
            "['Language Arts & Disciplines']","['Crafts & Hobbies']","['Education']","['Comics & Graphic Novels']","['Music']","['Medical']","['Pets']","['True Crime']","['Literary Collections']",
            "['Detective and mystery stories']","['Gardening']","[""Children's stories""]","['Foreign Language Study']","['Animals']","['House & Home']","['Technology & Engineering']",
            "['Adventure stories']","['Games & Activities']","['Photography']","['Games']","['Friendship']","['Law']","['Architecture']","['American fiction']","['Christian life']",
            "['Brothers and sisters']","['Mathematics']","['Cats']","['English fiction']","['Antiques & Collectibles']","['Families']","['English language']","['Bible']","['Domestic fiction']",
            "['Dogs']","['England']","['Adolescence']","['Science fiction']","['Australia']","['African Americans']","['Design']","['Adventure and adventurers']","['Great Britain']",
            "['Fantasy fiction']","['United States']","['Christmas stories']","['Children']","['Bears']","['Conduct of life']","['Authors, American']","['Fantasy']","['Fairy tales']",
            "['American poetry']","['Romance fiction']","['Actors']","[""Children's stories, American""]","['Transportation']","['French fiction']","['German fiction']","['Horror tales']",
            "['Dinosaurs']","['Murder']","['France']","['Canada']","['Babysitters']","['Man-woman relationships']","['American literature']","['FICTION']","['Adultery']",
            "[""Children's stories, American.""]","['Christian fiction']","['City and town life']","['Indians of North America']","['Brothers']","[""Children's stories, English""]",
            "['Horror stories.']","['Death']","['Americans']","['Study Aids']","['Authors, English']","['Science fiction, American']","['Ghost stories']","['Bibles']","['Africa']","['Angels']",
            "[""Children's literature""]","['Schools']"]

            otherCategories = {'1':"['Miscellaneous 1']", '2':"['Miscellaneous 2']", '3':"['Miscellaneous 3']", '4':"['Miscellaneous 4']", '5':"['Miscellaneous 5']",
                                '6':"['Miscellaneous 6']", '7':"['Miscellaneous 7']", '8':"['Miscellaneous 8']", '9':"['Miscellaneous 9']", '0':"['Miscellaneous 10']"}


            preprocessedData.loc[(preprocessedData['Category'].isin(mostPopularCategories)),'Restricted-Category'] = preprocessedData['Category']

            # Assign books with unpopular categories to one out of ten 'Miscellaneous' categories.

            for x in range(10):
                preprocessedData.loc[(~preprocessedData['Category'].isin(mostPopularCategories)) & (preprocessedData.index % 10 == x),'Restricted-Category'] = otherCategories.get(str(x))



            # Write DataFrame to a csv file
            preprocessedData.to_csv(path_or_buf=self.current_directory + '/Preprocessed_books_formatted.csv', sep=';',line_terminator='\n', quotechar='"', quoting=csv.QUOTE_ALL, index = False, columns= ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L', 'Category', 'Restricted-Category', 'Summary', 'Language'] )



    def formatPreprocessedRatings(self):
        if not(os.path.exists(self.current_directory + '/Preprocessed_Ratings_formatted.csv')):

            preprocessedData = pd.read_csv(self.current_directory + '/Preprocessed_data.csv', sep=',', encoding="latin-1", on_bad_lines='skip', quotechar = '"')


            preprocessedData.drop(columns = ['id', 'location','age', 'book_title', 'book_author', 'year_of_publication', 'publisher', 'img_s', 'img_m', 'img_l', 'Summary', 'Language', 'Category' ,'city','state','country'],axis=1,inplace = True)

            preprocessedData.rename(columns = {'user_id':'User-ID', 'isbn':'ISBN', 'rating':'Book-Rating'}, inplace=True)


            preprocessedData.drop_duplicates(subset=['ISBN', 'User-ID'], keep='first', inplace=True, ignore_index=True)


            preprocessedData.to_csv(path_or_buf=self.current_directory + '/Preprocessed_Ratings_formatted.csv', sep=';',line_terminator='\n', quotechar='"', quoting=csv.QUOTE_ALL, index = False, columns= ['User-ID', 'ISBN', 'Book-Rating'] )


    def formatRatings(self):

        if not(os.path.exists(self.current_directory + "/BX-Book-Ratings_formatted.csv")):

            preprocessedData = pd.read_csv(self.current_directory + '/BX-Book-Ratings.csv', sep=';', encoding="latin-1", on_bad_lines='skip', quotechar = '"')
            books = pd.read_csv(self.current_directory + '/BX_Books_formatted.csv', sep=';', encoding="latin-1", on_bad_lines='skip', quotechar = '"')
            isbns = books['ISBN'].unique()

            ratings= preprocessedData[(preprocessedData['ISBN'].isin(isbns))]
            ratings = ratings.head(1000)

            ratings.to_csv(path_or_buf=self.current_directory + '/BX-Book-Ratings_formatted.csv', sep=';',line_terminator='\n', quotechar='"', quoting=csv.QUOTE_ALL, index = False, columns= ['User-ID', 'ISBN', 'Book-Rating'])

        print("finished loading ratings")



    def get_book_categories(self, row):
        """Get Category from the Google books API"""

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

    def formatBooks(self):

        if not(os.path.exists(self.current_directory + "/BX_Books_formatted.csv")):

            df = pd.read_csv(self.current_directory + '/Preprocessed_Books_formatted.csv', sep=';', encoding="latin-1", on_bad_lines='skip', quotechar = '"')
            BXdf = pd.read_csv(self.current_directory + '/BX_Books.csv', sep=';', encoding="latin-1", on_bad_lines='skip', quotechar = '"')
            isbns = BXdf['ISBN'].unique()

            BXdf = pd.merge(BXdf, df, how='left', on=None, sort=False, copy=False, indicator=False, validate=None)

            BXdf = BXdf.drop_duplicates(subset=['ISBN'], keep='first')
            BXdf = BXdf.head(200000)

            BXdf.to_csv(path_or_buf=self.current_directory + '/BX_Books_formatted.csv', sep=';',line_terminator='\n', quotechar='"', quoting=csv.QUOTE_ALL, index = False, columns= ['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L', 'Category', 'Restricted-Category', 'Summary', 'Language'] )


        print("The book csv has been formatted")


    def loadBooks(self):

        ratingsDataset = 0
        self.isbn_to_title = {}
        self.title_to_isbn = {}

        reader = Reader(line_format = 'user item rating', sep=';', skip_lines = 1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader = reader)

        with open(self.booksPath, newline = '\n', encoding= 'ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile, delimiter=";", quotechar='"')
            next(bookReader)

            for row in bookReader:
                isbn = row[0]
                title = row[1]
                self.isbn_to_title[isbn] = title
                self.title_to_isbn[title] = isbn

        print("The books have been loaded")

        return ratingsDataset


    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(self.ratingsPath, newline='\n') as csvfile:
            ratingReader = csv.reader(csvfile,  delimiter=";")
            next(ratingReader)

            for row in ratingReader:
                userID = int(row[0])
                if(user == userID):
                    isbn = row[0]
                    rating = float(row[2])
                    userRatings.append((isbn, rating))
                    hitUser = True
                if (hitUser and(user != userID)):
                    break

        return userRatings



    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile,   delimiter=";")
            next(ratingReader)
            for row in ratingReader:
                isbn = row[1]
                ratings[isbn] += 1
        rank = 1
        for isbn, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[isbn] = rank
            rank += 1
        return rankings

    def getGenres(self):
        genres = defaultdict(list)
        genreIDs = {}
        maxGenreID = 0
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile,   delimiter=";", quotechar='"')
            next(bookReader)
            for row in bookReader:
                isbn = row[0]
                genreList = row[8].split(',')
                genreIDList = []
                for genre in genreList:
                    if genre in genreIDs:
                        genreID = genreIDs[genre]
                    else:
                        genreID = maxGenreID
                        genreIDs[genre] = genreID
                        maxGenreID += 1
                    genreIDList.append(genreID)
                genres[isbn] = genreIDList

        for (isbn, genreIDList) in genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
            genres[isbn] = bitfield

        return genres

    def getYears(self):
        years = defaultdict(int)
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile, delimiter = ';', quotechar= '"')
            next(bookReader)
            for row in bookReader:
                isbn = row[0]
                title = row[1]
                year = row[3]
                if year:
                    years[isbn] = int(year)
        return years

    def getBookTitle(self, isbn):
        if isbn in self.isbn_to_title:
            return self.isbn_to_title.get(isbn)
        else:
            return ""

    def getisbn(self, title):
        if title in self.title_to_isbn:
            return self.title_to_isbn.get(title)
        else:
            return 0


test = ProcessData()
# # test.formatBooks()
test.formatRatings()
#
# data = test.loadBooks()

# ratings = test.getUserRatings(276725)
# print(ratings)

# genres = test.getGenres()
# print(genres)
#
# years = test.getYears()
# print(years)
#
# ranks = test.getPopularityRanks()
# print(ranks)
#
# print(test.title_to_isbn)
# print(test.isbn_to_title)
# print(test.getBookTitle("0002005018"))
# print(test.getisbn('Clara Callan'))
