"""This recommender uses the 'BX_Books.csv', 'BX-Users.csv' and 'BX-Book-Ratings.csv' datasets to give content based recommendations """
import os
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

database_directory = "/home/nithila/SEG-major-project/clubs/book_database"
# books = pd.read_csv("Preprocessed_data.csv")
books = pd.read_csv(database_directory + "/BX_Books.csv", sep=';', encoding="latin-1", on_bad_lines='skip', quotechar='"')
users = pd.read_csv(database_directory + "/BX-Users.csv", sep=';', encoding="latin-1", on_bad_lines='skip', quotechar='"')
ratings = pd.read_csv(database_directory + "/BX-Book-Ratings.csv", sep=';', encoding="latin-1", on_bad_lines='skip', quotechar='"')
books = books[["ISBN", 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L']]
books.rename(columns = {'ISBN':'isbn', 'Book-Title':'book_title', 'Book-Author':'book_author', 'Year-Of-Publication':'year', 'Publisher':'publisher', 'Image-URL-S':'img_s', 'Image-URL-M':'img_m', 'Image-URL-L':'img_l'}, inplace=True)
users.rename(columns = {'User-ID':'user_id', 'Location':'location', 'Age':'age'}, inplace=True)
ratings.rename(columns = {'User-ID':'user_id', 'ISBN':'isbn', 'Book-Rating':'rating'}, inplace=True)

# print(list(books.columns))
# print(books)
# print(list(users.columns))
# print(users)
# print(list(ratings.columns))
# print(ratings)

users_with_ratings = users.merge(ratings, on='user_id')
merged_contents = users_with_ratings.merge(books, on='isbn')

# print(list(merged_contents.columns))
# print(merged_contents)

df = merged_contents.copy()
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

df.drop(columns = ['location','isbn', 'img_s','img_m','age',],axis=1,inplace = True)


df.drop(index=df[df['rating'] == 0].index, inplace=True)

# print(list(df.columns))
# print (df)



def content_based_recommender(book_title):

    book_title = str(book_title)
    if book_title in df['book_title'].values:
        rating_counts = pd.DataFrame(df['book_title'].value_counts())
        rare_books = rating_counts[rating_counts['book_title'] <= 100].index
        common_books = df[~df['book_title'].isin(rare_books)]

        if book_title in rare_books:

            random = pd.Series(common_books['book_title'].unique()).sample(5).values
            print('There are no recommendations for this book')
            print('Try: \n')
            print('{}'.format(random[0]),'\n')
            print('{}'.format(random[1]),'\n')
            print('{}'.format(random[2]),'\n')
            print('{}'.format(random[3]),'\n')
            print('{}'.format(random[4]),'\n')
        else:

            common_books = common_books.drop_duplicates(subset=['book_title'])
            common_books.reset_index(inplace= True)
            common_books['index'] = [i for i in range(common_books.shape[0])]
            target_cols = ['book_title','book_author','publisher']
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
      print('Cant find book in dataset, please check spelling')

book1 = content_based_recommender("The Color Purple")
print(book1)
book2 = content_based_recommender("The Testament")
print(book2)
book3 = content_based_recommender("1st to Die: A Novel")
print(book3)
book4 = content_based_recommender("Harry Potter and the Order of the Phoenix (Book 5)")
print(book4)
book5 = content_based_recommender("Fahrenheit 451")
print(book5)
