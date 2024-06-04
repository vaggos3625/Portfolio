import pandas as pd
import numpy as np
import pickle
import random
from sklearn.metrics.pairwise import cosine_similarity

user_movie_less_20 = pd.read_csv('/home/evangelo/decision-dill-student-code/week10/df_user_movie_less_20.csv')
movies = pd.read_csv('/home/evangelo/Downloads/ml-latest-small/movies.csv')

#random_5 = movies.title.sample(5)

def recommender_cosine(new_user_ratings):
    new_user = np.zeros_like(user_movie_less_20.columns)
    for index, item in enumerate(user_movie_less_20.columns):
    #print(index,item)
        if new_user_ratings.get(item): # <-- Return the value for key if key is in the dictionary
            #print(index, item)
            new_user[index] = new_user_ratings[item]
            
    new_user_df = pd.DataFrame([new_user],index = ['new_user'],columns= user_movie_less_20.columns)
    updated_df = pd.concat([new_user_df, user_movie_less_20]).iloc[:50, :50]
    updated_df_t = updated_df.T
    updated_cosine_sim_table = pd.DataFrame(cosine_similarity(updated_df), index=updated_df.index, columns=updated_df.index)        
    
    active_user = 'new_user'
    unseen_movies = list(updated_df_t.index[updated_df_t[active_user] == 0])
    neighbours = list(updated_cosine_sim_table[active_user].sort_values(ascending=False).index[1:4])
    
    predicted_ratings_movies = []
    for movie in unseen_movies:
    
        # we check the users who watched the movie
        people_who_have_seen_the_movie = list(updated_df_t.columns[updated_df_t.loc[movie] > 0])
    
        num = 0
        den = 0
        for user in neighbours:
            # if this person has seen the movie
            if user in people_who_have_seen_the_movie:
            #  we want to extract the ratings and similarities
                rating = updated_df_t.loc[movie, user]
                similarity = updated_cosine_sim_table.loc[active_user, user]
            
            # predict the rating based on the (weighted) average ratings of the neighbours
            # sum(ratings)/no.users OR 
            # sum(ratings*similarity)/sum(similarities)
                num = num + rating*similarity
                den = den + similarity
        if den != 0:
            predicted_ratings = num/den
        else:
            predicted_ratings = 0
        predicted_ratings_movies.append([predicted_ratings,movie])
        
        
    df_pred = pd.DataFrame(predicted_ratings_movies,columns = ['rating','movie'])
    df_pred = df_pred.sort_values(by=['rating'],ascending=False)['movie']
    return(df_pred.iloc[1:6])
