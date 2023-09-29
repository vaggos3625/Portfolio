import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF
import pickle
from sklearn.preprocessing import StandardScaler

movies = pd.read_csv('/home/evangelo/Downloads/ml-latest-small/movies.csv')
ratings = pd.read_csv('/home/evangelo/decision-dill-student-code/week10/ratings.csv')

R = csr_matrix((ratings['rating'], (ratings['userId'], ratings['movieId'])))
model_0 = NMF(n_components=50, init='nndsvd', max_iter=10000, tol=0.01, verbose=2)
model_0.fit(R)
P = model_0.transform(R)
Q = model_0.components_

with open('./nmf_recommender.pkl', 'wb') as file:
    pickle.dump(model_0, file)

with open('./nmf_recommender.pkl', 'rb') as file:  # This "with open" mimic is a so-called "context manager".
    model = pickle.load(file)

def recommend_nmf(query, model, k=10):
    """
    Filters and recommends the top k movies for any given input query based on a trained NMF model. 
    Returns a list of k movie ids.
    """
    # 1. candidate generation
    data = list(query.values())   # the ratings of the new user
    row_ind = [0]*len(data)       # we use just a single row 0 for this user 
    col_ind = list(query.keys())
    
    # construct a user vector
    R_user = csr_matrix((data, (row_ind, col_ind)), shape = (1, R.shape[1]))
    P_user = model.transform(R_user)
    R_recommended = np.dot(P_user, Q)

    # 2. scoring
    scores = model.inverse_transform(model.transform(R_user))
    scores = pd.Series(scores[0])
    # calculate the score with the NMF model

    # 3. ranking
    scores = scores.sort_values(ascending=False)
    collection = scores.head(20).index
    recommendations = []
    # filter out movies allready seen by the user
    for i in collection:
        if i not in query.keys():
            recommendations.append(i)
    recommendations = pd.DataFrame(movies.set_index('movieId').loc[recommendations].title)
    # return the top-k highst rated movie ids or titles
    print('These are the top 10 recommended movies for the user:', recommendations[:10] )
    #for i in recommendations:
    return recommend_nmf

recommend_nmf({8:2, 42:4, 444: 3, 122:1, 569:4}, model)