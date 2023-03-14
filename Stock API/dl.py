#Data Layer
import os
import pymongo

client = pymongo.MongoClient(os.getenv('URL_MONGODB'))
db = client['stock']

#Get data from db
def get_data(collection, query, sort):
    data = list(db[collection].find(query).sort(sort))
    return data

def insert_data(collection, data):
    ids = db[collection].insert_many(data)
    return ids

def update_data(collection, query, data):
    db[collection].update_one(query,data)

def update_many_data(collection, query, data):
    db[collection].update_many(query,data)

def delete_data(collection, query):
    db[collection].delete_one(query)

def delete_many_data(collection, query):
    db[collection].delete_many(query)