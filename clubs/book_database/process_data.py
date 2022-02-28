import os
import csv
import system
import re
from surprise import Dataset
from surprise import reader
from collections import defaultdict
import numpy as np

class ProcessData:

    isbn_to_name = {}
    name_to_isbn = {}
    ratingsPath = '../clubs/book_database/BX-Book-Ratings.csv'
    booksPath = '../clubs/book_database/books_with_categories.csv'

    def loadBooks(self):

        os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.isbn_to_title = {}
        self.title_to_isbn = {}

        reader = Reader(line_format = 'user item rating', sep=';', skip_lines = 1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader = reader)

        with open(self.booksPath, newline = '\n', encoding= 'ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)

            for row in bookReader:
                isbn = row[0]
                bookTitle = row[1]
                self.isbn_to_title[isbn] = bookTitla
                self.title_to_isbn[bookName] = isbn

        return ratingsDataset


    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(slef.ratingsPath, newline='\n') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)

            for row in ratingReader:
                userID = int(row[0])
                if(user == userID):
                    isbn = row[0]
                    rating = float(row[2])
                    userRatings.append(isbn, rating)
                    hitUser = True
                if (hitUser and(user != userID)):
                    break

        return userRatings



    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
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
            bookReader = csv.reader(csvfile)
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
            genres[movieID] = bitfield

        return genres

    def getYears(self):
        years = defaultdict(int)
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
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
            return self.title_to_isbn[isbn]
        else:
            return ""

    def getisbn(self, title):
        if title in self.title_to_isbn:
            return self.isbn_to_title[title]
        else:
            return 0
