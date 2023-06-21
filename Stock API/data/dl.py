#Data Layer
import os
import pymongo

client = pymongo.MongoClient(os.getenv('URL_MONGODB'))
db = client['stock']
class dl_base:
#Get data from db
    def get_data(collection, query, sort=None):
        if sort:
            result = db[collection].find(query).sort(sort)
        else:
            result = db[collection].find(query)
        data_response = []
        for data in result:
            data['_id'] = str(data['_id'])
            data_response.append(data)
        return list(data_response)

    def get_data_limit(collection, query, sort, limit):
        result = db[collection].find(query).sort(sort).limit(limit)
        for data in result:
            data['_id'] = str(data['_id'])
        return list(result)

    def get_data_one(collection, query):
        data = db[collection].find_one(query)
        if data:
            data['_id'] = str(data['_id'])
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