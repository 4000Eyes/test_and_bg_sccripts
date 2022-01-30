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

val = input("Are you sure you want to run this script?")
if val == "yes":
    x = input("Running this script will delete data. Are you sure?")
    if x == "yes":
        print ("I am inside the script")
        db = connect_to_mongo()
        delete_user(db,"user")
        delete_user(db,"approval_queue")
        delete_user(db, "notification_and_recommendation")
    else:
        exit(1)
exit(1)