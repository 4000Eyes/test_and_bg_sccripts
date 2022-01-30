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

current_date_time =  datetime.now(tz=pytz.UTC).strftime("%d-%m-%Y %H-%M-%S")
site_url = os.environ.get("API_URL")


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
        client = pymongo.MongoClient(db_string)
        db = client.get_database("sample_airbnb")
        return db
    except Exception as e:
        print("The generic error is", e)
        return None
    except errors.PyMongoError as e:
        print("The error message is ", e)
        return None

def occasion_reminder():
    try:
        mongo_db_handle = connect_to_mongo()
        if mongo_db_handle is None:
            print ("Unable to connect to mongo db")
        graph_db_handle = connect_to_graph()
        if graph_db_handle is None:
            print ("Unable to connect to graph db")

        first_reminder_date = get_date(int(os.environ.get("REMINDER_PRIMARY_OFFSET")))

        query = "MATCH (u:User)-[rr]->(fc:friend_circle)<-[yy]->(fl:friend_list), (fo:friend_occasion), (o:occasion) " \
                " where fc.friend_circle_id = fo.friend_circle_id " \
                " and type(rr) = 'CIRCLE_CREATOR'" \
                " and fo.occasion_id = o.occasion_id " \
                " return " \
                "u.first_name as creator_first_name," \
                "u.last_name as creator_last_name," \
                "u.user_id as creator_user_id," \
                "fl.user_id as sc_user_id, " \
                "fl.linked_user_id as sc_linked_user_id, " \
                "fl.first_name as sc_first_name," \
                "fl.last_name as sc_last_name," \
                " fo.occasion_date, " \
                " fo.occasion_name, " \
                " type(yy) as sc_relationship_type," \
                " type(rr) as creator_relationship_type," \
                " case type(yy) when 'SECRET_FRIEND' then 1 else 0 end as rel_flag, " \
                " fc.friend_circle_id as friend_circle_id ," \
                " duration.inDays(date(datetime({epochmillis: apoc.date.parse(fo.created_dt, 'ms', 'dd/MM/yyyy HH:mm:ss')})), date()).days as days_since " \
                " order by fc.friend_circle_id," \
                " rel_flag desc "
              # " WHERE apoc.temporal.format(fo.occasion_date, 'dd-MMM-yyyy') = apoc.temporal.format($ddate_) "

        driver = graph_db_handle.session()
        result = driver.run(query)
        temp_friend_circle_id = None
        secret_user_id = None
        secret_first_name = None
        secret_last_name = None
        secret_linked_user_id = None
        rn_collection = pymongo.collection.Collection(mongo_db_handle, "birthday_reminder")
        for row in result:
            if not temp_friend_circle_id or temp_friend_circle_id != row["friend_circle_id"]:
                if row["rel_flag"] == 1:
                    secret_user_id = row["sc_user_id"]
                    secret_first_name = row["sc_first_name"]
                    secret_last_name = row["sc_last_name"]
                    secret_linked_user_id = row["sc_linked_user_id"]

                    result = rn_collection.insert_one({"creator_user_id":row["creator_user_id"],
                                                   "creator_first_name":row["creator_first_name"],
                                                    "creator_last_name" : row["creator_last_name"],
                                                   "friend_circle_id" : row["friend_circle_id"],
                                                   "secret_user_id" : row["sc_user_id"],
                                                   "secret_first_name" : row["sc_first_name"],
                                                   "secret_last_name" : row["sc_last_name"],
                                                   "secret_linked_user_id" : row["sc_linked_user_id"],
                                                   "status" : 0,
                                                   "action_taken" : 0,
                                                   "day_since_created" : row["days_since"],
                                                   "entered_dt" : current_date_time})
                else:
                    result = rn_collection.insert_one({"creator_user_id":row["sc_user_id"],
                                                       "creator_first_name":row["sc_first_name"],
                                                        "creator_last_name" : row["sc_last_name"],
                                                       "friend_circle_id" : row["friend_circle_id"],
                                                       "secret_user_id" : secret_user_id,
                                                       "secret_first_name" : secret_first_name,
                                                       "secret_last_name" : secret_last_name,
                                                       "secret_linked_user_id" : secret_linked_user_id,
                                                       "status" : 0,
                                                       "action_taken" : 0,
                                                       "day_since_created": row["days_since"],
                                                       "entered_dt" : current_date_time})

    except neo4j.exceptions.Neo4jError as e:
        print ("The error is", e)
        return False
    except pymongo.errors as e:
        print ("The error is ", e)
        return False
    except Exception as e:
        print ("The error is", e)
        return False


occasion_reminder()
print ("I am done")


# activities to app notify in the initial phase
# occasion reminders
# interest reminders
# relationship reminders ( age, relationship)
# approvals


# user_collection = airbnb.get_collection("user")
#
# with client.start_session() as session:
#     session.start_transaction()
#     result = user_collection.find()
#     for row in result:
#         print(row)
#     session.commit_transaction()
#
# db_handle = client.get_database("sample_airbnb")
#
# return db_handle