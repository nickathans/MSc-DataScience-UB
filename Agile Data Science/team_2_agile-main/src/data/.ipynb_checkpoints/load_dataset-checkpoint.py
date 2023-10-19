import yaml
import argparse
import pickle

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
    file_data = open(external_path, 'rb') 
    movielens = pickle.load(file_data)
    
    #saving raw
    file_data = open(raw_path, 'wb') 
    pickle.dump(movielens, file_data)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_data(config_path=parsed_args.config)