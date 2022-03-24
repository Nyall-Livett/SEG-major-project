from process_data_content_based import ProcessData
from content_based_KNN import ContentKNNAlgorithm
from evaluator import Evaluator
from surprise import NormalPredictor

import random
import numpy as np

def LoadBookData():
    book_ratings = ProcessData()
    print("Loading book ratings...")
    book_data = book_ratings.loadBooks()
    print("\nComputing book popularity ranks so we can measure novelty later...")
    rankings = book_ratings.getPopularityRanks()
    return (book_ratings, book_data, rankings)

np.random.seed(0)
random.seed(0)

# Load up common data set for the recommender algorithms
(book_data, evaluationData, rankings) = LoadBookData()

# Construct an Evaluator to, you know, evaluate them
evaluator = Evaluator(evaluationData, rankings)

contentKNN = ContentKNNAlgorithm()

evaluator.AddAlgorithm(contentKNN, "ContentKNN")

# Just make random recommendations
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")

evaluator.Evaluate(False)

evaluator.SampleTopNRecs(book_data)
