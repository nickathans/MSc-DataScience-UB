import os
import argparse
import pandas as pd
import numpy as np
import pickle
from load_dataset import read_params
from spotlight.cross_validation import user_based_train_test_split






def split_and_saved_data(config_path):
    """
    split the train dataset(data/raw) and save it in the data/processed folder
    input: config path 
    output: save splitted files in output folder
    """
    config = read_params(config_path)
    raw_data_path = config["raw_data_config"]["raw_path"]
    test_percentage = config["raw_data_config"]["test_percentage"]
    random_state = config["raw_data_config"]["random_state"] 
    train_data_path = config["processed_data_config"]["train_data"]
    test_data_path = config["processed_data_config"]["test_data"] 
    
    
    #loading raw
    file_data = open(raw_data_path, 'rb') 
    raw_data = pickle.load(file_data)
    
    train, test = user_based_train_test_split(raw_data,test_percentage=test_percentage,random_state=np.random.RandomState(random_state))
    
    #saving train, test
    file_data = open(train_data_path, 'wb') 
    pickle.dump(train, file_data)
    
    file_data = open(test_data_path, 'wb') 
    pickle.dump(test, file_data)
    
    
if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)