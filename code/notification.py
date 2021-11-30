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

def insert_notification_for_primary_reminder():
    try:
        mongo_db_handle = connect_to_mongo()
        if mongo_db_handle is None:
            print ("Unable to connect to mongo db")
        graph_db_handle = connect_to_graph()
        if graph_db_handle is None:
            print ("Unable to connect to graph db")

        first_reminder_date = get_date(int(os.environ.get("REMINDER_PRIMARY_OFFSET")))
        query = "MATCH  (u:User)-[yy]->(fc:friend_circle)<-[rr]->(fl:friend_list), (fx:friend_occasion) " \
                "WHERE EXISTS " \
                "{ MATCH (fo:friend_occasion) " \
                " WHERE apoc.temporal.format(fo.occasion_date, 'dd-MMM-yyyy') = apoc.temporal.format($ddate_) " \
                " AND fo.friend_circle_id = fc.friend_circle_id } and" \
                " AND type(yy) = 'CIRCLE_CREATOR'" \
                " AND fx.friend_circle_id = fc.friend_circle_id " \
                " RETURN  fx.occasion_name, fl.friend_id, fl.user_id, fl.first_name, fl.last_name, u.user_id, " \
                "u.first_name, u.last_name, type(yy) as creator_rel, type(rr) as con_sec_rel" \
                " ORDER BY type(rr) DESC"

        result = graph_db_handle.run(query, ddate_ = first_reminder_date)
        temp_user_id = None
        secret_user_id = None
        rn_collection = pymongo.collection.Collection(mongo_db_handle, "notification_and_recommendation")
        for row in result:
            # do something
            if not temp_user_id or temp_user_id != row["u.user_id"]:
                temp_user_id = row["u.user_id"]
                secret_user_id = row["con_sec_rel"]
                if secret_user_id != "SECRET_FRIEND":
                    return False
                if os.environ.get("REMINDER_PRIMARY_OFFSET") is None:
                    return False
                message = "Reminder" + row["fl.first_name"] + "'s " + row["fo.occasion_name"] + " is " + os.environ.get("REMINDER_PRIMARY_OFFSET") + " days away "
                message += " Click here to find the right gift"
                result = rn_collection.insert_one({"user_id":row["u.user_id"],
                                                   "first_name":row["u.first_name"],
                                                   "transaction_type":"Reminder",
                                                   "message": message,
                                                   "entered_dt" : current_date_time})
                if result is None:
                    return False
            else:
                result = rn_collection.insert_one({"user_id": row["fl.user_id"],
                                               "first_name": row["fl.first_name"],
                                               "transaction_type": "Reminder",
                                               "message": message,
                                               "entered_dt": current_date_time})
                if result is None:
                    return False
    except pymongo.errors as e:
        print ("The error is ", e)
        return False
    except neo4j.exceptions.Neo4jError as e:
        print ("The error is", e)
        return False
    except Exception as e:
        print ("The error is", e)
        return False


def insert_notification_for_secondary_reminder():
    try:
        mongo_db_handle = connect_to_mongo()
        if mongo_db_handle is None:
            print("Unable to connect to mongo db")
        graph_db_handle = connect_to_graph()
        if graph_db_handle is None:
            print("Unable to connect to graph db")

        if os.environ.get("REMINDER_SECONDARY_OFFSET") is None:
            return False
        first_reminder_date = get_date(int(os.environ.get("REMINDER_SECONDARY_OFFSET")))
        query = "MATCH  (u:User)-[yy]->(fc:friend_circle)<-[rr]->(fl:friend_list), (fx:friend_occasion) " \
                "WHERE EXISTS " \
                "{ MATCH (fo:friend_occasion) " \
                " WHERE apoc.temporal.format(fo.occasion_date, 'dd-MMM-yyyy') = apoc.temporal.format($ddate_) " \
                " AND fo.friend_circle_id = fc.friend_circle_id } and" \
                " AND type(yy) = 'CIRCLE_CREATOR'" \
                " AND fx.friend_circle_id = fc.friend_circle_id " \
                " RETURN  fx.occasion_name, fl.friend_id, fl.user_id, fl.first_name, fl.last_name, u.user_id, " \
                "u.first_name, u.last_name, type(yy) as creator_rel, type(rr) as con_sec_rel" \
                " ORDER BY type(rr) DESC"

        result = graph_db_handle.run(query, ddate_=first_reminder_date)
        temp_user_id = None
        secret_user_id = None
        rn_collection = pymongo.collection.Collection(mongo_db_handle, "notification_and_recommendation")
        for row in result:
            # do something
            if not temp_user_id or temp_user_id != row["u.user_id"]:
                temp_user_id = row["u.user_id"]
                secret_user_id = row["con_sec_rel"]
                if secret_user_id != "SECRET_FRIEND":
                    return False
                message = "Reminder" + row["fl.first_name"] + "'s " + row["fo.occasion_name"] + " is " + os.environ.get(
                    "REMINDER_PRIMARY_OFFSET") + " days away "
                message += " Click here to find the right gift"
                result = rn_collection.insert_one({"user_id": row["u.user_id"],
                                                   "first_name": row["u.first_name"],
                                                   "transaction_type": "Reminder",
                                                   "message": message,
                                                   "entered_dt": current_date_time})
                if result is None:
                    return False
            else:
                result = rn_collection.insert_one({"user_id": row["fl.user_id"],
                                                   "first_name": row["fl.first_name"],
                                                   "transaction_type": "Reminder",
                                                   "message": message,
                                                   "entered_dt": current_date_time})
                if result is None:
                    return False
    except pymongo.errors as e:
        print("The error is ", e)
        return False
    except neo4j.exceptions.Neo4jError as e:
        print("The error is", e)
        return False
    except Exception as e:
        print("The error is", e)
        return False

def insert_birthday_ecard_confirmation():
    return True

def insert_interest_survey():
    return True

def insert_product_survey():
    return True

def insert_relationship_gaps():
    query = " match (fl:friend_list),(fc:friend_circle) where  (fl)-[:CONTRIBUTOR]->(fc) and not (fl)-[:RELATED]->(fc)  return fl.user_id, fc.friend_circle_id order by fc.friend_circle_id"

def insert_interest_reminders():
    try:
        mongo_db_handle = connect_to_mongo()
        if mongo_db_handle is None:
            print("Unable to connect to mongo db")
        graph_db_handle = connect_to_graph()
        if graph_db_handle is None:
            print("Unable to connect to graph db")

        if os.environ.get('INTEREST_THRESHOLD') is None:
            return False
        reminder_date = get_date(os.environ.get(('INTEREST_THRESHOLD')))
        query = "MATCH (fc:friend_circle)<-[yy]-(fl:friend_list)-[r:INTEREST]->(sc:WebSubCat), (u:User) " \
                " WHERE apoc.temporal.format(r.created_dt, 'MMM-dd-yyyy' ) =  apoc.temporal.format($reminder_date_) " \
                " AND u.user_id = fl.friend_id " \
                " AND yy = 'CONTRIBUTOR' " \
                " RETURN fl.user_id, fl.first_name, fl.last_name, sc.subcategory_name, u.user_id, u.first_name, u.last_name"

        result = graph_db_handle.run(query, reminder_date_ = reminder_date)
        return True
    except Exception as e:
        return False

insert_notification_for_primary_reminder()
insert_notification_for_secondary_reminder()
insert_birthday_ecard_confirmation()
