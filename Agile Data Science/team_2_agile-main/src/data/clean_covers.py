import numpy as np
import pandas as pd
import requests
import time

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

def fill_missing_range(df, field, range_from, range_to, range_step=1, fill_with=0):
    return df\
      .merge(how='right', on=field,
            right = pd.DataFrame({field:np.arange(range_from, range_to, range_step)}))\
      .sort_values(by=field).reset_index().fillna(fill_with).drop(['index'], axis=1)

if __name__ == "__main__":
    poster_cols = ['movie_id', 'cover_link']
    posters = pd.read_csv('../../data/external/movie_poster.csv', names=poster_cols,
                        encoding='latin-1')
#    print(posters.cover_link.shape)
#    for link in posters.cover_link[:20]:
#        if not is_url_image(link):
#            print(link)
#        time.sleep(3)
    posters = fill_missing_range(posters, 'movie_id', 1, 1683, 1, 'https://dummyimage.com/800x1200/5f5f5f/fff.jpg&text=NO+COVER')
    posters.to_csv('../../data/external/movie_poster_clean.csv', index=False, header=False)
