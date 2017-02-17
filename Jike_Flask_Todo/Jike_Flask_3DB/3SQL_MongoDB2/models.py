import pymongo

def get_conn():
    client = pymongo.MongoClient('127.0.0.1',27017)
    db = client.jikexueyuan
    user = db.user_collection
    return user

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email


    def save(self):
        user = {"name" : self.name, "email":self.email}
        coll = get_conn()
        id = coll.insert(user)
        print id


    @staticmethod
    def query_user():
        users = get_conn().find()
        return users