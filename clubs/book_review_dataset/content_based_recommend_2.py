"""This uses the 'preprocessed_data.csv' dataset to give recommendation. 'preprocessed_data.csv' contains genre data and a brief summary of the books"""
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


books = pd.read_csv(os.getcwd() +"/clubs/book_review_dataset/final3.csv")
# print(books)



df = books.copy()
# df.dropna(inplace=True)
# df.reset_index(drop=True, inplace=True)
# df.drop(columns = ['Unnamed: 0','location','isbn',
#                    'img_s','img_m','city','age',
#                    'state','Language','country',
#                    'year_of_publication'],axis=1,inplace = True)
# df.drop(index=df[df['Category'] == '9'].index, inplace=True) #remove 9 in category

# df.drop(index=df[df['rating'] == 0].index, inplace=True) #remove 0 in rating

# df['Category'] = df['Category'].apply(lambda x: re.sub('[\W_]+',' ',x).strip())


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
            # print('There are no recommendations for this book')
            # print('Try: \n')
            # print('{}'.format(random[0]),'\n')
            # print('{}'.format(random[1]),'\n')
            # print('{}'.format(random[2]),'\n')
            # print('{}'.format(random[3]),'\n')
            # print('{}'.format(random[4]),'\n')
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
    #   print('Cant find book in dataset, please check spelling')
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
            # print('There are no recommendations for this book')
            # print('Try: \n')
            # print('{}'.format(random[0]),'\n')
            # print('{}'.format(random[1]),'\n')
            # print('{}'.format(random[2]),'\n')
            # print('{}'.format(random[3]),'\n')
            # print('{}'.format(random[4]),'\n')
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
    #   print('Cant find book in dataset, please check spelling')
        random = list(pd.Series(common_books['book_title'].unique()).sample(5).values)
        return random



# print("recommendation based on book title, author, publisher and category")
# print(content_based_recommender("Husband, Lover, Stranger (Husband, Lover, Stranger)"))
# print(content_based_recommender("The Testament"))
# print(content_based_recommender("1st to Die: A Novel"))
# print(content_based_recommender("Harry Potter and the Order of the Phoenix (Book 5)"))
# print(content_based_recommender("Fahrenheit 451"))
# print(content_based_recommender("The Street Lawyer"))
# print(content_based_recommender("Divine Secrets of the Ya-Ya Sisterhood: A Novel"))
# print(content_based_recommender("To Kill a Mockingbird"))
# print(content_based_recommender("A Walk to Remember"))
# print(content_based_recommender("A Painted House"))
# print(content_based_recommender("The Summons"))
# print(content_based_recommender("Snow Falling on Cedars"))
# print(content_based_recommender("Tuesdays with Morrie: An Old Man, a Young Man, and Life's Greatest Lesson"))
# print(content_based_recommender("Girl with a Pearl Earring"), '\n')

# print(content_based_recommender("Dreamcatcher"))
# print(content_based_recommender_2("Dreamcatcher"))


# print("recommendation based on summary")
# print(content_based_recommender_2("Husband, Lover, Stranger (Husband, Lover, Stranger)"))
# print(content_based_recommender_2("The Testament"))
# print(content_based_recommender_2("1st to Die: A Novel"))
# print(content_based_recommender_2("Harry Potter and the Order of the Phoenix (Book 5)"))
# print(content_based_recommender_2("Fahrenheit 451"))
# print(content_based_recommender_2("The Street Lawyer"))
# print(content_based_recommender_2("Divine Secrets of the Ya-Ya Sisterhood: A Novel"))
# print(content_based_recommender_2("To Kill a Mockingbird"))
# print(content_based_recommender_2("A Walk to Remember"))
# print(content_based_recommender_2("A Painted House"))
# print(content_based_recommender_2("The Summons"))
# print(content_based_recommender_2("Snow Falling on Cedars"))
# print(content_based_recommender_2("Tuesdays with Morrie: An Old Man, a Young Man, and Life's Greatest Lesson"))
# print(content_based_recommender_2("Girl with a Pearl Earring"))
