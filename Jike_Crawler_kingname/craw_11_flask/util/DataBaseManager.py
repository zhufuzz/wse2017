import pymongo

class DataBaseManager(object):
    def __init__(self):
        connection = pymongo.MongoClient()
        tdb = connection.webControl
        self.post_info = tdb.test

    def insert(self, info):
        self.post_info.insert(info)
