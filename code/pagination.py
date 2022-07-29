from pymongo import errors, MongoClient
import pymongo.collection
import os
import requests
code_environment = os.environ.get("BG_ENVIRON")

def get_data(skip_count):
    try:
        email_sent_hash = {}
        client = MongoClient(db_string)
        result = []
        x = client.get_database("sample_airbnb")
        result = pymongo.collection.Collection(x, "user").find().skip(skip_count).limit(5)
        for row in result:
            print ("The row value is", row)
    except Exception as e:
        print ("The error is ", e)


if code_environment == "test":
    db_string = os.environ.get("MONGO_TEST")
get_data(5)
get_data(10)
get_data(15)
