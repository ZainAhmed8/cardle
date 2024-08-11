from pymongo import MongoClient

client = MongoClient("mongodb+srv://zainahmed8:9xohXdECeL337HLM@cardlecluster.0nj0jgx.mongodb.net/CardleMain")

db = client['CardleMain']
collection = db['cardle_coll']
dist_countries = collection.distinct("country")
print(dist_countries)