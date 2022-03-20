from .process_data import ProcessData
from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
from ..models import Book

def generate_recommendations(user_id):

    user = f'{user_id}'
    k = 10


    book_ratings = ProcessData()
    book_data = book_ratings.loadBooks()

    trainSet = book_data.build_full_trainset()

    sim_options = {'name': 'msd',
                   'user_based': False
                   }

    model = KNNBasic(sim_options=sim_options)
    model.fit(trainSet)
    simsMatrix = model.compute_similarities()

    testUserInnerID = trainSet.to_inner_uid(user)

    # Get the top K items we rated
    testUserRatings = trainSet.ur[testUserInnerID]
    kNeighbors = heapq.nlargest(k, testUserRatings, key=lambda t: t[1])

    # Not getting the top N books, we try to get all the books with rating
    # higher than 8.0

    # kNeighbors = []
    # for rating in testUserRatings:
    #     if rating[1] > 8.0:
    #         kNeighbors.append(rating)

    # Get similar items to stuff we liked (weighted by rating)
    candidates = defaultdict(float)
    for itemID, rating in kNeighbors:
        similarityRow = simsMatrix[itemID]
        for innerID, score in enumerate(similarityRow):
            candidates[innerID] += score * (rating / 10.0)

    # Build a dictionary of stuff the user has already seen
    watched = {}
    for itemID, rating in trainSet.ur[testUserInnerID]:
        watched[itemID] = 1

    # Get top-rated items from similar users:
    pos = 0
    recommendations = []
    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if not itemID in watched:
            isbn = trainSet.to_raw_iid(itemID)
            #print(isbn)
            #print(ml.getMovieName(int(movieID)), ratingSum)
            # print(book_ratings.getBookTitle(isbn), ratingSum)
            book = Book.objects.get(isbn = isbn)
            recommendations.append(book)
            pos += 1
            if (pos > 10):
                break

    return recommendations
