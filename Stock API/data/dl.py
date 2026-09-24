# Data Layer
import os
import pymongo

client = pymongo.MongoClient(os.getenv("URL_MONGODB"))
db = client["stock"]

_INSERT_BATCH = 8000


class dl_base:
    def get_data(collection, query, sort=None):
        if sort:
            result = db[collection].find(query).sort(sort)
        else:
            result = db[collection].find(query)
        data_response = []
        for data in result:
            data["_id"] = str(data["_id"])
            data_response.append(data)
        return list(data_response)

    def get_docs(collection, query=None, sort=None, projection=None):
        proj = {"_id": 0} if projection is None else projection
        cursor = db[collection].find(query or {}, proj)
        if sort:
            cursor = cursor.sort(sort)
        return list(cursor)

    def get_data_limit(collection, query, sort, limit):
        result = db[collection].find(query).sort(sort).limit(limit)
        for data in result:
            data["_id"] = str(data["_id"])
        return list(result)

    def get_data_one(collection, query):
        data = db[collection].find_one(query)
        if data:
            data["_id"] = str(data["_id"])
        return data

    def insert_data(collection, data):
        if not data:
            return None
        col = db[collection]
        last = None
        for i in range(0, len(data), _INSERT_BATCH):
            last = col.insert_many(data[i : i + _INSERT_BATCH], ordered=False)
        return last

    def replace_collection(collection, data, indexes=None):
        db[collection].drop()
        dl_base.insert_data(collection, data)
        if indexes:
            for index in indexes:
                db[collection].create_index(index)

    def replace_dataframe(collection, df, indexes=None):
        db[collection].drop()
        if df is None or df.height == 0:
            if indexes:
                for index in indexes:
                    db[collection].create_index(index)
            return
        col = db[collection]
        for batch in df.iter_slices(_INSERT_BATCH):
            records = batch.to_dicts()
            if records:
                col.insert_many(records, ordered=False)
        if indexes:
            for index in indexes:
                db[collection].create_index(index)

    def update_data(collection, query, data):
        db[collection].update_one(query, data)

    def update_many_data(collection, query, data):
        db[collection].update_many(query, data)

    def delete_data(collection, query):
        db[collection].delete_one(query)

    def delete_many_data(collection, query):
        db[collection].delete_many(query)

    def drop(collection):
        db[collection].drop()

    def create_indexes(collection, indexes):
        for index in indexes:
            db[collection].create_index(index)
