import yaml
import argparse
import pickle
import pandas as pd
import numpy as np
from spotlight.interactions import Interactions

def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    try:
        with open(config_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
            return config
    except OSError:
        return "Error loading file"

def load_data(config_path):
    config = read_params(config_path)
    external_path = config["external_data"]
    raw_path = config["raw_data_config"]["raw_path"]

    #loading external
    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings = pd.read_csv(external_path, sep='\t', names=r_cols,encoding='latin-1')
    
    movielens = Interactions(np.int32(ratings['user_id'].values),np.int32(ratings['movie_id'].values),np.int32(ratings['rating'].values),np.int32(ratings['unix_timestamp'].values))

    #saving raw
    file_data = open(raw_path, 'wb') 
    pickle.dump(movielens, file_data)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_data(config_path=parsed_args.config)