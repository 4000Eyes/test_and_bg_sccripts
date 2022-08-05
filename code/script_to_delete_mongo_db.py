import neo4j.exceptions
from neo4j import GraphDatabase
from pymongo import errors, MongoClient
import pymongo
import pymongo.collection
import pymongo.client_session
import pytz
from datetime import datetime, tzinfo, timedelta
import os
import requests
import json

def connect_to_mongo():
    code_environment = os.environ.get("BG_ENVIRON")
    if code_environment == "test":
        db_string = os.environ.get("MONGO_TEST")
    try:
        client = pymongo.MongoClient(db_string)
        db = client.get_database("sample_airbnb")
        return db
    except Exception as e:
        print("The generic error is", e)
        return None
    except errors.PyMongoError as e:
        print("The error message is ", e)
        return None

def delete_user(db_handle, collection_name):
    try:
        mongo_user = pymongo.collection.Collection(db_handle, collection_name)
        mongo_user.delete_many({})

        return True
    except pymongo.errors as e:

        print("The error is ", e)
        return False
    except Exception as e:

        print("The error is ", e)
        return False

print ("The script has started")
db = connect_to_mongo()
val = input("Are you sure you want to run this script?")
if val == "yes":
    x = input("Running this script will delete data. Are you sure?")
    if x == "yes":
        print ("I am inside the script")
        y = input("Type the table id: product(1), user(2), approval queue(3), notification(4), gemift_messages(5) interests(6")
        if int(y) == 1:
            delete_user(db, "gemift_product_db")
        if int(y) == 2:
            delete_user(db,"user")
        if int(y) == 3:
            delete_user(db,"approval_queue")
        if int(y) == 4:
            delete_user(db, "notification_and_recommendation")
        if int(y) == 5:
            delete_user(db,"gemift_messages")
        if int(y) == 6:
            delete_user(db,"interests")
    else:
        exit(1)
exit(1)