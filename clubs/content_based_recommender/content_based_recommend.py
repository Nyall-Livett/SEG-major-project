
# import ssl
# try:
#      _create_unverified_https_context =     ssl._create_unverified_context
# except AttributeError:
#      pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
import re
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
# nltk.download("stopwords")
# nltk.download("punkt")
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


books = pd.read_csv(os.getcwd() +"/clubs/content_based_recommender/data_set_smaller.csv")




df = books.copy()


"""Uses book title, author, publisher and Category to give recommendations"""
def content_based_recommender(book_title):

    book_title = str(book_title)
    rating_counts = pd.DataFrame(df['book_title'].value_counts())
    rare_books = rating_counts[rating_counts['book_title'] <= 100].index
    common_books = df[~df['book_title'].isin(rare_books)]
    common_books = common_books.drop_duplicates(subset=['book_title'])
    common_books.reset_index(inplace= True)
    if book_title in df['book_title'].values:

        if book_title in rare_books:

            random = list(pd.Series(common_books['book_title'].unique()).sample(5).values)
            return random
        else:
            common_books['index'] = [i for i in range(common_books.shape[0])]
            target_cols = ['book_title','book_author','publisher', 'Category']
            common_books['combined_features'] = [' '.join(common_books[target_cols].iloc[i,].values) for i in range(common_books[target_cols].shape[0])]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(common_books['combined_features'])
            cosine_sim = cosine_similarity(count_matrix)
            index = common_books[common_books['book_title'] == book_title]['index'].values[0]
            sim_books = list(enumerate(cosine_sim[index]))
            sorted_sim_books = sorted(sim_books,key=lambda x:x[1],
                                      reverse=True)[1:6]

            books = []
            for i in range(len(sorted_sim_books)):
                books.append(common_books[common_books['index'] == sorted_sim_books[i][0]]['book_title'].item())

            return books

    else:
        random = list(pd.Series(common_books['book_title'].unique()).sample(5).values)
        return random

"""Uses brief summary of the book to give recommendations"""
def content_based_recommender_2(book_title):
    book_title = str(book_title)
    rating_counts = pd.DataFrame(df['book_title'].value_counts())
    rare_books = rating_counts[rating_counts['book_title'] <= 100].index
    common_books = df[~df['book_title'].isin(rare_books)]
    common_books = common_books.drop_duplicates(subset=['book_title'])
    common_books.reset_index(inplace= True)
    if book_title in df['book_title'].values:
        if book_title in rare_books:

            random = list(pd.Series(common_books['book_title'].unique()).sample(5).values)
            return random
    
        else:
            common_books['index'] = [i for i in range(common_books.shape[0])]

            summary_filtered = []
            for i in common_books['Summary']:
                i = re.sub("[^a-zA-Z]"," ",i).lower()
                i = nltk.word_tokenize(i)
                i = [word for word in i if not word in set(stopwords.words("english"))]
                i = " ".join(i)
                summary_filtered.append(i)

            common_books['Summary'] = summary_filtered
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(common_books['Summary'])
            cosine_sim = cosine_similarity(count_matrix)
            index = common_books[common_books['book_title'] == book_title]['index'].values[0]
            sim_books = list(enumerate(cosine_sim[index]))
            sorted_sim_books = sorted(sim_books,key=lambda x:x[1],reverse=True)[1:6]
            books = []
            for i in range(len(sorted_sim_books)):
                books.append(common_books[common_books['index'] == sorted_sim_books[i][0]]['book_title'].item())
            return books

    else:
        random = list(pd.Series(common_books['book_title'].unique()).sample(5).values)
        return random



