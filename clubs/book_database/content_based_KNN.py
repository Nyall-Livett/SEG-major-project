from surprise import AlgoBase
from surprise import PredictionImpossible
from process_data import ProcessData
import math
import numpy as np
import heapq

class ContentKNNAlgorithm(AlgoBase):

    def __init__(self, k=40, sim_options={}):
        AlgoBase.__init__(self)
        self.k = k

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        # Compute item similarity matrix based on content attributes

        # Load up genre vectors for every book
        bookdata = ProcessData()
        genres = bookdata.getGenres()
        years = bookdata.getYears()

        print("Computing content-based similarity matrix...")

        # Compute genre distance for every book combination as a 2x2 matrix
        self.similarities = np.zeros((self.trainset.n_items, self.trainset.n_items))

        for thisRating in range(self.trainset.n_items):
            if (thisRating % 100 == 0):
                print(thisRating, " of ", self.trainset.n_items)
            for otherRating in range(thisRating+1, self.trainset.n_items):
                thisisbn = int(self.trainset.to_raw_iid(thisRating))
                otherisbn = int(self.trainset.to_raw_iid(otherRating))
                genreSimilarity = self.computeGenreSimilarity(thisisbn, otherisbn, genres)
                yearSimilarity = self.computeYearSimilarity(thisisbn, otherisbn, years)
                #mesSimilarity = self.computeMiseEnSceneSimilarity(thisisbn, otherisbn, mes)
                self.similarities[thisRating, otherRating] = genreSimilarity * yearSimilarity
                self.similarities[otherRating, thisRating] = self.similarities[thisRating, otherRating]

        print("...done.")

        return self

    def computeGenreSimilarity(self, book1, book2, genres):
        genres1 = genres[book1]
        genres2 = genres[book2]
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(genres1)):
            x = genres1[i]
            y = genres2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y

        return sumxy/math.sqrt(sumxx*sumyy)

    def computeYearSimilarity(self, book1, book2, years):
        diff = abs(years[book1] - years[book2])
        sim = math.exp(-diff / 10.0)
        return sim



    def estimate(self, u, i):

        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unkown.')

        # Build up similarity scores between this item and everything the user rated
        neighbors = []
        for rating in self.trainset.ur[u]:
            genreSimilarity = self.similarities[i,rating[0]]
            neighbors.append( (genreSimilarity, rating[1]) )

        # Extract the top-K most-similar ratings
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[0])

        # Compute average sim score of K neighbors weighted by user ratings
        simTotal = weightedSum = 0
        for (simScore, rating) in k_neighbors:
            if (simScore > 0):
                simTotal += simScore
                weightedSum += simScore * rating

        if (simTotal == 0):
            raise PredictionImpossible('No neighbors')

        predictedRating = weightedSum / simTotal

        return predictedRating
