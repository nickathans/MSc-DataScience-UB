import pymongo
import datetime
import requests
import json
import pandas as pd

credentials = {}
# MongoDB Credentials
credentials['MONGOPASS'] = "assignment1"
credentials['MONGOUSER'] = "dbUser"
credentials['MONGODB'] = "admin"

# Database and collection creation
def createDB(url):
    try:
        conn=pymongo.MongoClient(url)
    except pymongo.errors.ConnectionFailure as e:
            print ("Could not connect to MongoDB: %s" % e) 
    db = conn["weather"]
    return db['USweather']

# URL for mongoDB Connection creation
def get_url():
    return "mongodb://"+credentials['MONGOUSER']+":"+credentials['MONGOPASS']+"@mongodb:27017/"+credentials["MONGODB"]+"?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false"
    

collection = createDB(get_url())


url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q":"53.1,-0.13"}

headers = {
    "X-RapidAPI-Key": "38a5646c14msh52471d769a1b4d3p19af9cjsn431621e7e1de",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# use the json.loads method to parse the response text into a JSON object
json_response = json.loads(response.text)
df = pd.read_csv('Top100-US.csv', delimiter=";")
print(df.head())

for index, row in df.iterrows():
    querystring["q"] = row["City"] + " " + str(row["Zip"])
    response = requests.request("GET", url, headers=headers, params=querystring)
    weather_data = json.loads(response.text)
    city_weather = {
        "zip": row["Zip"],
        "city": row["City"],
        "created_at": datetime.datetime.utcnow(),
        "weather": weather_data
    }
    print(city_weather)
    collection.insert_one(city_weather)
