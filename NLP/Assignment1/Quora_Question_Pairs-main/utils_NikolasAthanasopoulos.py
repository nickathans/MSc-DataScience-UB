import pandas as pd
import scipy
import sklearn
from sklearn import *
import numpy as np
import os

# Build a function cast_list_as_strings that casts each element in the input list to a string.
def cast_list_as_strings(mylist):
    """
    return a list of strings
    """
    #assert isinstance(mylist, list), f"the input mylist should be a list it is {type(mylist)}"
    mylist_of_strings = []
    for x in mylist:
        mylist_of_strings.append(str(x))

    return mylist_of_strings


#Make a function get_features_from_df that given a dataframe containing the format of the train data it returns a scipy sparse matrix with the features from question 1 and question 2
def get_features_from_df(df, count_vectorizer):
    """
    returns a sparse matrix containing the features build by the count vectorizer.
    Each row should contain features from question1 and question2.
    """
    q1_casted =  cast_list_as_strings(list(df["question1"]))
    q2_casted =  cast_list_as_strings(list(df["question2"]))
    
    ############### Begin exercise ###################
    # what is kaggle                  q1
    # What is the kaggle platform     q2
    X_q1 = count_vectorizer.transform(q1_casted)
    X_q2 = count_vectorizer.transform(q2_casted)
    
    X_q1q2 = scipy.sparse.hstack((X_q1,X_q2))
    ############### End exercise ###################

    return X_q1q2


# Make a function get_mistakes that given a model clf a dataframe df, the features X_q1q2 and the target labels y returns
# incorrect_indices: coordinates where the model made a mistake
# predictions: predictions made by the model
def get_mistakes(clf, X_q1q2, y):

    ############### Begin exercise ###################
    predictions = clf.predict(X_q1q2)
    incorrect_predictions = predictions != y 
    incorrect_indices,  = np.where(incorrect_predictions)
    
    ############### End exercise ###################
    
    if np.sum(incorrect_predictions)==0:
        print("no mistakes in this df")
    else:
        return incorrect_indices, predictions
    

#def print_mistake_k(k, mistake_indices, predictions):
#    print(train_df.iloc[mistake_indices[k]].question1)
#    print(train_df.iloc[mistake_indices[k]].question2)
#    print("true class:", train_df.iloc[mistake_indices[k]].is_duplicate)
#    print("prediction:", predictions[mistake_indices[k]])