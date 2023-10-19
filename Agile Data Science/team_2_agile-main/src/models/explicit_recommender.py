from spotlight.cross_validation import random_train_test_split
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel
from spotlight.evaluation import sequence_mrr_score
import torch
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

def train_explicit(config_path):
    config = read_params(config_path)
    train_data_path = config["processed_data_config"]["train_data"]
    test_data_path = config["processed_data_config"]["test_data"] 
    explicit_path = config["models_dir"]["explicit"]
    loss = config["explicit_model"]["loss"]
    embedding_dim = config["explicit_model"]["embedding_dim"]
    n_iter = config["explicit_model"]["n_iter"]
    batch_size = config["explicit_model"]["batch_size"]
    l2 = config["explicit_model"]["l2"]
    learning_rate = config["explicit_model"]["learning_rate"]
    

    #loading train,test
    file_data = open(train_data_path, 'rb') 
    train = pickle.load(file_data)
    
    file_data = open(test_data_path, 'rb') 
    test = pickle.load(file_data)
    
    
    ################### MLFLOW ###############################
    mlflow_config = config["mlflow_config"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment(mlflow_config["experiment_explicit"])
    
    with mlflow.start_run(run_name=mlflow_config["run_name"]) as mlops_run:
        model = ExplicitFactorizationModel(loss=loss,
                                   embedding_dim=embedding_dim,
                                   n_iter=n_iter,
                                   batch_size=batch_size,
                                   l2=l2,
                                   learning_rate=learning_rate,
                                   use_cuda=torch.cuda.is_available())
        
        model.fit(train, verbose=True)
        train_rmse = rmse_score(model, train)
        test_rmse = rmse_score(model, test)
        print('Train RMSE {:.3f}, test RMSE {:.3f}'.format(train_rmse, test_rmse))
        
        mlflow.log_param("loss", loss)
        mlflow.log_param("embedding_dim", embedding_dim)
        mlflow.log_param("n_iter", n_iter)
        mlflow.log_param("batch_size",batch_size)
        mlflow.log_param("l2", l2)
        mlflow.log_param("learning_rate", learning_rate)

        mlflow.log_metric("train_rmse", train_rmse)
        mlflow.log_metric("test_rmse", test_rmse)
        
        #Saving the model
        file_model = open(explicit_path, 'wb') 
        pickle.dump(model, file_model)
    

def get_user_recommendations(movies_df, user_id):
    num_recommendations = 5
    
    #Loading the model
    file_model = open('models/explicit_model.pkl', 'rb') 
    model = pickle.load(file_model)

    predictions = model.predict(user_ids=user_id)
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
    train_explicit(config_path=parsed_args.config)