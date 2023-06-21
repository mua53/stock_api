import os
import pymongo
from data.dl import dl_base

client = pymongo.MongoClient(os.getenv('URL_MONGODB'))
db = client['stock']

class fliter_dl(dl_base):
    def get_last_date():
        return db['indicators'].find({},{'DTYYYYMMDD':1}).sort([('DTYYYYMMDD', -1)])