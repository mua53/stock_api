import os
import pymongo
from data.dl import dl_base

client = pymongo.MongoClient(os.getenv('URL_MONGODB'))
db = client['stock']

class calculate_dl(dl_base):

    def get_distint(collection, field):
        result = db[collection].distinct(field)
        return result