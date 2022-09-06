import json
from datetime import datetime
from pymongo import MongoClient, errors
import pymongo
import requests
import uuid
from datetime import datetime, date
import os
flag = 0
request_id = 0
merch_hash = {}
web_category_hash = {}
web_subcategory_hash = {}
brand_hash = {}
merch_web_hash = {}
web_sub_hash = {}
sub_brand_hash = {}

def insert_interests_mongo(interest_id, value, description, parent_id, age_lo, age_hi, gender, image_url):
    try:
        interest_collection = pymongo.collection.Collection(db_handle, "interests")

        interest_collection.insert_one({"interest_id": str(interest_id),
                                                 "interest_name": value,
                                                 "interest_description": description,
                                                 "age_lo": age_lo,
                                                 "age_hi": age_hi,
                                                 "gender": gender,
                                                 "parent_id": parent_id,
                                                 "inserted_date": current_date,
                                                 "image_url": image_url
                                                 })

        return True
    except Exception as e:
        print("The error is ", e)
        return False
def insert_entities(request_id, interest_id, value, description, parent_id, age_lo, age_hi, gender, image_url):
    parameters = {
        "request_id": request_id,
        "web_subcategory_id": str(interest_id),
        "value": value,
        "description": description,
        "parent_id": parent_id,
        "age_lo":age_lo,
        "age_hi":age_hi,
        "gender":gender,
        "image_url": image_url
    }
    response = requests.post("http://0.0.0.0:8081/api/category", json=parameters)
    print("The status code is", response.status_code)
    return response

def load_subcategories(file_path, file_name ):
    try:
        exception_file_name = file_name + datetime.now().strftime("%d-%m-%Y") + ".excep"
        output_file_name = file_name + datetime.now().strftime("%d-%m-%Y") + ".out"
        json_obj = open(file_path+ file_name, "r")
        ex_file_name = open(file_path + exception_file_name, "w")
        op_file_name = open(file_path + output_file_name, "w")
        data = json.load(json_obj)
        parent_id = None
        INSERT_SUBCATEGORY_REQUEST_ID = 3
        for i in data['subcategories']:
            interest_id = uuid.uuid4()
            res = insert_entities(INSERT_SUBCATEGORY_REQUEST_ID, interest_id, i["web_subcategory_name"], i["description"], i["parent_id"], i["age_lo"],i["age_hi"], i["gender"], i["image_url"])
            if res.status_code != 200:
                ex_file_name.write ("Unable to insert the subcategory row with subcategory_name", i["web_subcategory_name"])
                return -1
            if not insert_interests_mongo(interest_id, i["web_subcategory_name"], i["description"], parent_id, i["age_lo"],i["age_hi"], i["gender"],i["image_url"]):
                ex_file_name.write("We have an issue writing to Mongo db")
                return -1
            #construct the output and store.
            subcategory_response = {}
            subcategory_response = json.loads(res.text)
            i.update(subcategory_response)
            json_output = json.dumps(i)
            op_file_name.write(json_output)
    except Exception as e:
        print ("Unable to load subcategories")
        return -1


today = date.today()
current_date =  today.strftime("%d/%m/%Y")
db_handle = None
def connect_to_mongo():
    try:
        client = MongoClient(os.environ.get("MONGO_TEST"))
        result = []
        db_handle = client.get_database("sample_airbnb")
        return db_handle
    except errors.PyMongoError as e:
        print("The error message is ", e)
        return None
    except Exception as e:
        print("The generic error is", e)
        return None



"""
output_list = []
parameters = {
    "request_id": 1
}
response = requests.get("http://0.0.0.0:8081/api/category", params=parameters)
print ("The response is ", response.json())
clist = []

dict_cat = {}
clist = json.loads(response.text)

for i in clist:
    dict_cat["web_category_name"] = i["web_category_id"]
parameters = {
    "request_id": 5
}
response = requests.get("http://0.0.0.0:8081/api/category", params=parameters)
print ("The response is ", response.json())
dict_json = {}
dict_json= json.loads(response.text)

dict_cat_subcat = {}
for i in dict_json["data"]:
    dict_cat_subcat[i["subcategory_name"]] = i
"""
file_path = '/home/krissrinivasan/'
file_name = 'Loves-Electronics-A121-subcategory.json'
db_handle = connect_to_mongo()
load_subcategories(file_path, file_name)

exit(0)

