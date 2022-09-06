from pymongo import errors, MongoClient
import pymongo
import os
_mdbconnection = None
def connect_to_mongo():
    try:
        global _mdbconnection
        if _mdbconnection is None:
            print("Getting connect string " + str(os.environ.get("MONGO_DB_NAME")))
            db_string = os.environ.get("MONGO_TEST")
            client = MongoClient(db_string)
            _mdbconnection = client.get_database(os.environ.get("MONGO_DB_NAME"))
            print("After getting mongo db connection" + str(_mdbconnection))
        return _mdbconnection
    except errors.PyMongoError as e:
        print("The error message is ", e)
        return None
    except Exception as e:
        print("The generic error is", e)
        return None

def sort_data_by_date(dbhandle):
    try:
        hsh_output = {}
        dbhandle = connect_to_mongo()
        message_collection = pymongo.collection.Collection(dbhandle, "gemift_messages")
        #result = message_collection.find({"$and": [{"user_id": user_id}, {"is_seen": "N"}]})
        result = message_collection.find().sort("kdate", pymongo.DESCENDING).limit(1)

        for rec in result:
            print ("The rows are ", rec)
        return True
    except Exception as e:
        print("The error in function get message count is " + e)
        return False

db_handle=None
sort_data_by_date(db_handle)