from pymongo import errors, MongoClient
import pymongo.collection
import os
import requests
code_environment = os.environ.get("BG_ENVIRON")

def send_email(parameters):
    try:
        output_list = []

        response = requests.post("http://0.0.0.0:8081/api/login", json=parameters)
        #response = requests.post("https://gemift.uw.r.appspot.com/api/auth/signup", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def get_referrer_user_info(user_id):
    try:
        client = MongoClient(db_string)
        result = []
        x = client.get_database("sample_airbnb")
        email_collection = pymongo.collection.Collection(x, "email_queue")
        result  = email_collection.aggregate([{"$match":{"email_sent_status":"N"}},
                                              {"$project":{"referrer_user_id":1, "referred_user_id":1, "email_address":1, "phone_number":1, "user_type":1, "comm_type":1}},
                                              {"$sort": {"referred_user_id": pymongo.ASCENDING}}
                                              ])
        return result
    except errors.PyMongoError as e:
        print("The error message is ", e)
        return None
    except Exception as e:
        print("The generic error is", e)
        return None

if code_environment == "test":
    db_string = os.environ.get("MONGO_TEST")

def send_email_to_new_users():
    try:
        email_sent_hash = {}
        client = MongoClient(db_string)
        result = []
        x = client.get_database("sample_airbnb")
        email_collection = pymongo.collection.Collection(x, "email_queue")
        result  = email_collection.aggregate([{"$match":{"email_sent_status":"N"}},
                                              {"$project":{"referrer_user_id":1, "referred_user_id":1, "email_address":1, "phone_number":1, "user_type":1, "comm_type":1}},
                                              {"$sort": {"referred_user_id": pymongo.ASCENDING}}
                                              ])

        for row in result:
            print ("The row is ", row["email_address"], row["referred_user_id"], row["phone_number"])
            parameters = {}
            if row["user_type"] == "New":
                if row["comm_type"] == "Email":
                    parameters["email_to"] = row["email_address"]
                    parameters["email_to_first_name"] = row["first_name"]
                    parameters["email_to_last_name"] = row["last_name"]
                    parameters["call_to_action"] = "None"
                    if send_email(parameters) != 200:
                        print("Unable to send email to ", row["email_address"])
                        exit(0)
                    print ("Sent email to ", row["email_address"])
                    email_sent_hash["email_address"] = "Y"
                else:
                    #whatsapp. Need figure this out. However, if there is a valid email send an invitation
                    if row["email_address"] is not None:
                        if email_sent_hash[row["email_address"]] == "Y":
                            continue
                        parameters["email_to"] = row["email_address"]
                        parameters["email_to_first_name"] = row["first_name"]
                        parameters["email_to_last_name"] = row["last_name"]
                        parameters["call_to_action"] = "None"
                        if send_email(parameters) != 200:
                            print("Unable to send email to ", row["email_address"])
                            exit(0)
                        email_sent_hash["email_address"] = "Y"
                        print("sent an email to whatsapp customer with email ", row["email_address"])
                    else:
                        print ("I need to figure out what to do when it is whatspp and no valid email exist")
            else:
                print ("I exist already")
            upd_email_queue = email_collection.update_one({"referred_user_id":row["referred_user_id"], "referrer_user_id":row["referrer_user_id"]},
                                                                    {"$set":{"email_status":"Y"}})
            if upd_email_queue is None:
                print ("Update didnt happen")
        print ("I am done")
    except errors.PyMongoError as e:
        print ("The error message is ", e)
    except Exception as e:
        print ("The generic error is", e)



def send_email_to_existing_users():
    try:
        referrer_user_id = None
        counter = 0
        parameters = {}
        client = MongoClient(db_string)
        result = []
        x = client.get_database("sample_airbnb")
        email_collection = pymongo.collection.Collection(x, "email_queue")
        result = email_collection.aggregate([{"$match": {"email_sent_status": "N"}},
                                             {"$project": {"referrer_user_id": 1, "referred_user_id": 1,
                                                           "email_address": 1, "phone_number": 1, "user_type": 1,
                                                           "comm_type": 1}},
                                             {"$sort": {"email_address": pymongo.ASCENDING}}
                                             ])

        for row in result:
          print("The row is ", row["email_address"], row["referred_user_id"], row["phone_number"])
          if row["user_type"] == "Existing":
            if counter == 0:
                parameters["email_to"] = row["email_address"]
                parameters["email_to_first_name"] = row["first_name"]
                parameters["email_to_last_name"] = row["last_name"]
                user_data = get_referrer_user_info(row["referrer_user_id"])
                if user_data is not None:
                    referrer_user_id = row["referrer_user_id"]
                    parameters["friend_names"] = row["first_name"]
                    counter = 1
                    continue
            if counter == 1:
                if parameters["email_to"] == row["email_address"]:
                    if referrer_user_id != row["referrer_user_id"]:
                        user_data = get_referrer_user_info(row["referrer_user_id"])
                        if user_data is not None:
                            referrer_user_id = row["referrer_user_id"]
                            parameters["friend_names"] = parameters["friend_names"] + " ," + row["first_name"]
                else:
                    if not send_email(parameters):
                        print ("Unable to send friend invitation email for ", parameters["email_to"])
                        exit(0)
                    parameters = {}
                    parameters["email_to"] = None # This is to avoid attribute not found error when comparing
                    referrer_user_id = None

        upd_email_queue = email_collection.update_one(
            {"referred_user_id": row["referred_user_id"]}, {"$set": {"email_status": "Y"}})
        if upd_email_queue is None:
            print("Update didnt happen")
        print("I am done")
    except errors.PyMongoError as e:
        print("The error message is ", e)
    except Exception as e:
        print("The generic error is", e)



"""
{"$group": {"_id": 0,
            "email_address": {'$addToSet': "$email_address"},
            "phone_number": {'$addToSet': "$phone_number"},
            "referred_user_id": {'$addToSet': "$referred_user_id"},
            "comm_type": {'$addToSet': "$comm_type"},
            "user_type": {'$addToSet': "$user_type"}
            }}
"""