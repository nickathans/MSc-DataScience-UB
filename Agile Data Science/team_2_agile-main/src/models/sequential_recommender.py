from spotlight.cross_validation import random_train_test_split
from spotlight.evaluation import rmse_score
from spotlight.sequence.implicit import ImplicitSequenceModel
from spotlight.evaluation import sequence_mrr_score
import argparse
import yaml
import numpy as np
import pandas as pd
import pickle
import mlflow

def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def train_sequential(config_path):
    config = read_params(config_path)
    train_data_path = config["processed_data_config"]["train_data"]
    test_data_path = config["processed_data_config"]["test_data"] 
    sequential_path = config["models_dir"]["sequential"]
    n_iter = config["sequential_model"]["n_iter"]
    representation = config["sequential_model"]["representation"]
    loss = config["sequential_model"]["loss"]
    
    

    #loading train,test
    file_data = open(train_data_path, 'rb') 
    train = pickle.load(file_data)
    
    file_data = open(test_data_path, 'rb') 
    test = pickle.load(file_data)
    
    train = train.to_sequence()
    test = test.to_sequence()
    
    ################### MLFLOW ###############################
    mlflow_config = config["mlflow_config"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment(mlflow_config["experiment_sequential"])
    
    with mlflow.start_run(run_name=mlflow_config["run_name"]) as mlops_run:
        model = ImplicitSequenceModel(n_iter=n_iter,
                                      representation=representation,
                                      loss=loss)
        
        model.fit(train, verbose=True)
        mrr_score_mean = np.mean(sequence_mrr_score(model, test))
        print(mrr_score_mean)
        
        mlflow.log_param("n_iter",n_iter)
        mlflow.log_param("representation", representation)
        mlflow.log_param("loss", loss)

        mlflow.log_metric("mrr_score_mean", mrr_score_mean)
        
        #Saving the model
        file_model = open(sequential_path, 'wb') 
        pickle.dump(model, file_model)
    

def get_recommendations(movies_df, movies_ids):
    num_recommendations = 5
    
    #Loading the model
    file_model = open('models/sequential_model.pkl', 'rb') 
    model = pickle.load(file_model)

    predictions = model.predict(sequences=np.array(movies_ids))
    indices = np.argsort(predictions)
    predictions[::-1].sort()
    
    # LOADING NECESSARY DATAFRAMES FOR MEAN RATING COLUMN
    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings = pd.read_csv('data/external/u.data', sep='\t', names=r_cols,
                      encoding='latin-1')
    m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']
    movies = pd.read_csv('data/external/u.item', sep='|', names=m_cols, usecols=range(5),
                         encoding='latin-1')

    poster_cols = ['movie_id', 'cover_link']
    posters = pd.read_csv('data/external/movie_poster_clean.csv', names=poster_cols,
                      encoding='latin-1')
    movie_ratings = pd.merge(movies, ratings)
    
    # directly obtaining the mean ratings
    ratings=movie_ratings[['title','rating']]
    ratings=ratings.groupby('title').mean()
    ratings.reset_index(inplace=True)
    ratings.rename(columns = {'rating':'mean_rating'}, inplace = True)
    
    df = pd.DataFrame()
    for i in range (0, num_recommendations):
        df = df.append(movies_df.iloc[indices[i]-1], ignore_index=True) 
    
    df.index = range(1,len(df)+1)
    # we get titles recommended by doing the intersection (they will always be in 'ratings')
    # this merge already includes the mean rating
    rating_aux=ratings.merge(df,how='inner',on=['title'])
    rating_aux=rating_aux.merge(posters,how='left',on=['movie_id'])
    #print(rating_aux['movie_id'])

    rating_aux=rating_aux.drop(['movie_id', 'release_date','video_release_date'], axis=1)

    # Increasing by 1 the indices
    rating_aux.index = range(1,len(rating_aux)+1) 
    
    return rating_aux.iloc[0:num_recommendations,:]
    

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_sequential(config_path=parsed_args.config)