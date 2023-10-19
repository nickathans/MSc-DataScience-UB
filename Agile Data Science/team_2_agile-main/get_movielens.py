from spotlight.datasets.movielens import get_movielens_dataset
import pickle

movielens = get_movielens_dataset(variant='100K')
file_data = open("Webapp/data/external/movielens.obj", 'wb') 
pickle.dump(movielens, file_data)