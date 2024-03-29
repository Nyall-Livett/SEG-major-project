import os
import csv
from surprise import Dataset
from surprise import Reader
from collections import defaultdict

class ProcessData:

    isbn_to_title = {}
    title_to_isbn = {}
    current_directory = os.getcwd()
    ratingsPath = current_directory + '/BX-Book-Ratings_formatted_evaluation.csv'
    booksPath = current_directory + '/BX_Books_formatted_evaluation.csv'

    def loadBooks(self):

        ratingsDataset = 0
        self.isbn_to_title = {}
        self.title_to_isbn = {}

        reader = Reader(line_format = 'user item rating', sep=';', skip_lines = 1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader = reader)

        with open(self.booksPath, newline = '\n', encoding= 'iso-8859-1') as csvfile:
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
        with open(self.booksPath, newline='', encoding='iso-8859-1') as csvfile:
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
        with open(self.booksPath, newline='', encoding='iso-8859-1') as csvfile:
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
            return f'{isbn}'

    def getisbn(self, title):
        if title in self.title_to_isbn:
            return self.title_to_isbn.get(title)
        else:
            return 0
