from process_data import ProcessData
from surprise import KNNBasic
from surprise import NormalPredictor
from evaluator import Evaluator

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
(book_ratings, book_data, rankings) = LoadBookData()

# Construct an Evaluator to, you know, evaluate them
evaluator = Evaluator(book_data, rankings)

# User-based cosine KNN
UserCosineKNN = KNNBasic(sim_options = {'name': 'cosine', 'user_based': True})
evaluator.AddAlgorithm(UserCosineKNN, "User Cosine KNN")

# User-based MSD KNN
UserMSDKNN = KNNBasic(sim_options = {'name': 'msd', 'user_based': True})
evaluator.AddAlgorithm(UserMSDKNN, "User MSD KNN")

# User-based Pearson KNN
UserPearsonKNN = KNNBasic(sim_options = {'name': 'pearson', 'user_based': True})
evaluator.AddAlgorithm(UserPearsonKNN, "User Pearson KNN")

# Item-based cosine KNN
ItemCosineKNN = KNNBasic(sim_options = {'name': 'cosine', 'user_based': False})
evaluator.AddAlgorithm(ItemCosineKNN, "Item Cosine KNN")

# Item-based MSD KNN
ItemMSDKNN = KNNBasic(sim_options = {'name': 'msd', 'user_based': False})
evaluator.AddAlgorithm(ItemMSDKNN, "Item MSD KNN")

# Item-based Pearson KNN
ItemPearsonKNN = KNNBasic(sim_options = {'name': 'pearson', 'user_based': False})
evaluator.AddAlgorithm(ItemPearsonKNN, "Item Pearson KNN")

# Just make random recommendations
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")

# Fight!
evaluator.Evaluate(False)

evaluator.SampleTopNRecs(book_ratings)
