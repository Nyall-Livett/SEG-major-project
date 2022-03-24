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
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')


class ProcessData:

    isbn_to_title = {}
    title_to_isbn = {}
    current_directory = os.getcwd()
    ratingsPath = current_directory + '/BX-Book-Ratings_formatted_smaller.csv'
    booksPath = current_directory +  '/BX_Books_formatted_smaller.csv'

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

    def getCombined(self):
        df = pd.read_csv(self.current_directory + '/BX_Books_formatted_smaller.csv', sep=';', encoding="iso-8859-1", on_bad_lines='skip', quotechar = '"')
        df['index'] = [i for i in range(df.shape[0])]
        target_cols = ['Book-Title','Book-Author','Publisher', 'Category']
        df = df.astype(str)
        df['combined_features'] = [' '.join(df[target_cols].iloc[i,].values) for i in range(df[target_cols].shape[0])]


        df = pd.Series(df.combined_features.values,index=df.ISBN).to_dict()

        return df

    def getSummary(self):
        df = pd.read_csv(self.current_directory + '/BX_Books_formatted_smaller.csv', sep=';', encoding="iso-8859-1", on_bad_lines='skip', quotechar = '"')


        df['index'] = [i for i in range(df.shape[0])]
        df = df.astype(str)

        summary_filtered = []
        for i in df['Summary']:
            i = re.sub("[^a-zA-Z]"," ",i).lower()
            i = nltk.word_tokenize(i)
            i = [word for word in i if not word in set(stopwords.words("english"))]
            i = " ".join(i)
            summary_filtered.append(i)

        df['Summary'] = summary_filtered
        df = pd.Series(df.Summary.values, index=df.ISBN).to_dict()

        return df

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
            return ""

    def getisbn(self, title):
        if title in self.title_to_isbn:
            return self.title_to_isbn.get(title)
        else:
            return 0