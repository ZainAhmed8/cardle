from pymongo import MongoClient

client = MongoClient("secret")

db = client['CardleMain']
collection = db['cardle_coll']
dist_countries = collection.distinct("country")
print(dist_countries)
