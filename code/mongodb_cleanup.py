import neo4j.exceptions
from neo4j import GraphDatabase
from pymongo import errors, MongoClient
import pymongo.collection
import pytz
from datetime import datetime, tzinfo, timedelta
import os


def connect_to_graph():
    try:
        driver = GraphDatabase.driver(os.environ.get("FTEYES_GDB_URI"), auth=(os.environ.get("FTEYES_GDB_USER"), os.environ.get("FTEYES_GDB_PWD")))
        return driver
    except neo4j.exceptions.Neo4jError as e:
        return None

def get_date(param):
    try:
        utc_now_dt = datetime.now(tz=pytz.UTC)
        formatted_datetime = utc_now_dt.strftime("%d-%m-%Y %H-%M-%S")
        current_date_time = datetime.strptime(formatted_datetime, "%d-%m-%Y %H-%M-%S")
        first_reminder_date = current_date_time + timedelta(days=int(param))
        return datetime.strftime(first_reminder_date, '%m-%d-%Y')
    except Exception as e:
        return None

def connect_to_mongo():
    code_environment = os.environ.get("BG_ENVIRON")
    if code_environment == "test":
        db_string = os.environ.get("MONGO_TEST")
    try:
        client = MongoClient(db_string)
        result = []
        db_handle = client.get_database("sample_airbnb")
        return db_handle
    except errors.PyMongoError as e:
        print("The error message is ", e)
        return None
    except Exception as e:
        print("The generic error is", e)
        return None

