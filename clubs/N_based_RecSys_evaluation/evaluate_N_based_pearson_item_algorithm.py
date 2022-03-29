from process_data import ProcessData
from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
from surprise.model_selection import LeaveOneOut
from recommender_metrics import RecommenderMetrics
from evaluation_data import EvaluationData

def LoadBookData():
    book_ratings = ProcessData()
    print("Loading book ratings...")
    book_data = book_ratings.loadBooks()
    print("\nComputing book popularity ranks so we can measure novelty later...")
    rankings = book_ratings.getPopularityRanks()
    return (book_ratings, book_data, rankings)

book_ratings, book_data, rankings = LoadBookData()

evalData = EvaluationData(book_data, rankings)

# Train on leave-One-Out train set
trainSet = evalData.GetLOOCVTrainSet()
sim_options = {'name': 'pearson',
               'user_based': False
               }

model = KNNBasic(sim_options=sim_options)
model.fit(trainSet)
simsMatrix = model.compute_similarities()

leftOutTestSet = evalData.GetLOOCVTestSet()

# Build up dict to lists of (isbn, predictedrating) pairs
topN = defaultdict(list)
k = 10
for uiid in range(trainSet.n_users):
    # Get top N similar users to this one
    userRatings = trainSet.ur[uiid]
    kNeighbors = heapq.nlargest(k, userRatings, key=lambda t: t[1])

    candidates = defaultdict(float)
    for itemID, rating in kNeighbors:
        similarityRow = simsMatrix[itemID]
        for innerID, score in enumerate(similarityRow):
            candidates[innerID] += score * (rating / 10.0)

    # Build a dictionary of stuff the user has already seen
    watched = {}
    for itemID, rating in trainSet.ur[uiid]:
        watched[itemID] = 1

    # Get top-rated items from similar users:
    pos = 0
    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if not itemID in watched:
            isbn = trainSet.to_raw_iid(itemID)
            topN[int(trainSet.to_raw_uid(uiid))].append( ((isbn), 0.0) )
            pos += 1
            if (pos > 40):
                break

# Measure
print("HR", RecommenderMetrics.HitRate(topN, leftOutTestSet))
