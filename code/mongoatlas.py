import json
import requests
import datetime

def search_product():
    try:
        parameters = {
            "request_id": 1,
            "age_floor" : 2,
            "age_ceiling": 32,
            "sort_order": "ASC",
            "occasion_list": ("Birthday","Marriage")
        }
        #response = requests.get("https://gemift.uw.r.appspot.com/api/prod/search", params=parameters)
        response = requests.get("http://0.0.0.0:8081/api/prod/search",params=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400


def search_product_detail():
    try:
        parameters = {
            "request_id": 7,
            "product_id" : (2,3)
        }
        #response = requests.get("https://gemift.uw.r.appspot.com/api/prod/search",params=parameters)
        response = requests.get("http://0.0.0.0:8081/api/prod/search",params=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def vote_product():
    try:
        parameters = {
            "request_id": 8,
            "product_id" : 2,
            "friend_circle_id":'95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "user_id" : '55e77082-d4c2-4bfa-8032-57f461765591',
            "friend_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "vote" : 1,
            "comment": "He will love this product",
            "occasion_name" : "birthday",
            "occasion_year": 2021
        }
        response = requests.get("http://localhost:5000/api/prod/search", json=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def get_product_votes():
    try:
        parameters = {
            "request_id": 5,
            "product_id" : 2,
            "friend_circle_id":'95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "occasion_name" : "birthday",
            "occasion_year": 2021
        }
        response = requests.get("http://localhost:5000/api/prod/search", json=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        print ("The toutput is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def test_get_web_category(request_id, age_lo, age_hi, gender):
    try:
        output_list = []
        parameters = {
            "request_id" : request_id,
            "age_lo" : age_lo,
            "age_hi" : age_hi,
            "gender" : gender
        }
        response = requests.get("http://localhost:5000/api/category", json=parameters)
        print ("The response is ", response.json())
        return 200
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def test_signup():
    try:
        output_list = []
        parameters = {
           # "email" : "Vidya1232@gmail.com",
            "email": "RamaKrishnaRamajayam@gmail.com",
            "user_type" : 0,
            "password" : "Buss",
            "phone_number" : "425-223-2233",
            "gender": "F",
            "first_name" : "Vidya",
            "last_name" : "Srinivasan",
            "external_referrer_id": "Amazon",
            "external_referrer_param": "abc123-1Njsh"
        }
        #response = requests.post("http://localhost:5000/api/auth/signup", json=parameters)
        response = requests.post("https://gemift.uw.r.appspot.com/api/auth/signup", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400

def friend_circle_request_1():
    try:
        output_list = []
        parameters = {
            "request_id" : 1,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "referrer_user_id" :'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "referred_user_id" : '54f2e35a-9786-4875-a202-ea0b762c8f07',
            "email_address":"k123@gmail.com",
            "phone_number": "425-111-2322",
            "first_name":"x",
            "last_name":"y",
            "gender": "M"
        }
        response = requests.post("http://localhost:5000/api/friend/circle", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def friend_circle_request_2():
    try:
        output_list = []
        parameters = {
            "request_id" : 2,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "referrer_user_id" :'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "referred_user_id" : '54f2e35a-9786-4875-a202-ea0b762c8f07',
            "email_address":"k1234@gmail.com",
            "phone_number": "425-111-2322",
            "first_name":"x",
            "last_name":"y",
            "gender": "M"
        }
        response = requests.post("http://localhost:5000/api/friend/circle", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False
def friend_circle_request_2():
    try:
        output_list = []
        parameters = {
            "request_id": 2,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "referrer_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "email_address": "r1234@gmail.com",
            "phone_number": "425-111-2322",
            "first_name": "x",
            "last_name": "y",
            "gender": "M"
        }
        response = requests.post("http://localhost:5000/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False
def friend_circle_request_3():
    try:
        output_list = []
        parameters = {
            "request_id": 3,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "referrer_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "referred_user_id": '54f2e35a-9786-4875-a202-ea0b762c8f07',
            "email_address": "k1234@gmail.com",
            "phone_number": "425-111-2322",
            "first_name": "x",
            "last_name": "y",
            "gender": "M"
        }
        response = requests.post("http://localhost:5000/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False


def friend_circle_request_4():
    try:
        output_list = []
        parameters = {
            "request_id": 4,
            "referrer_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "email_address": "vedu1234@gmail.com",
            "phone_number": "425-111-2322",
            "first_name": "Vidya",
            "last_name": "Krishnan",
            "gender": "F"
        }
        response = requests.post("http://localhost:5000/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_friend_circle():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86'
        }
        response = requests.get("http://localhost:5000/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_friend_circles():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c'
        }
        response = requests.get("http://localhost:5000/api/friend/circle", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False
def add_interest():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "creator_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "user_id": 'fd28bcef-ff38-453a-9258-41e00d6fe6b1',
            "list_category_id": [{"web_category_id":"c3e3805c-8d4a-4bb1-9cb4-7d1d4f05b682", "vote":1}, {"web_category_id":"067da0e1-dc08-4ecf-a6c9-a403611c1886", "vote":1}],
            "list_subcategory_id" :[{"web_subcategory_id":"6a0f5478-b1b0-48b0-9e86-3f5bf44682c0", "vote":1}]
        }
        response = requests.post("http://localhost:5000/api/interest", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_interest():
    try:
        output_list = []
        parameters = {
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86'
        }
        response = requests.get("http://localhost:5000/api/interest", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def create_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "creator_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "contributor_user_id":'54f2e35a-9786-4875-a202-ea0b762c8f07',
            "occasion_id" : 1,
            "occasion_date" : "01/02/2000"
        }
        response = requests.post("http://localhost:5000/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def vote_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 2,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "creator_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "contributor_user_id":"f800d518-248c-41d6-bd62-6cf9cad2b9e3",
            "occasion_id" : 1,
            "flag": 1,
            "value": "I agree with this date"
        }
        response = requests.post("http://localhost:5000/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def approve_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 3,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86',
            "creator_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "contributor_user_id": 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "occasion_id":1,
            "flag": 1
        }
        response = requests.post("http://localhost:5000/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def get_occasion():
    try:
        output_list = []
        parameters = {
            "request_id": 1,
            "friend_circle_id": '95b38dd9-bdcf-40d6-8a69-4ed50cce4e86'
        }
        response = requests.get("http://localhost:5000/api/user/occasion", json=parameters)
        print("The response is ", response.json())
        return response.status_code
    except Exception as e:
        return False

def test_whatsapp():
    try:
        output_list = []
        parameters = {
            "admin_friend_id" : 'f7d403d9-ceb4-4e47-b074-db8c70427f7c',
            "request_id" : 5,
            "user_list" : [
                    {"email_address":"k1@gmail.com", "phone_number": "425-111-1111", "first_name":"x", "last_name":"y", "gender": "M"},
                {"email_address": "k2@gmail.com", "phone_number": "425-111-1112", "first_name": "a", "last_name": "b",
                 "gender": "M"},
                {"email_address": "k3@gmail.com", "phone_number": "425-111-1113", "first_name": "a", "last_name": "d",
                 "gender": "M"},
                           ]
        }
        response = requests.post("http://localhost:5000/api/friend/circle", json=parameters)
        print ("The response is ", response.json())
        return response.status_code
    except Exception as e:
        print("There is an exception with the request", e)
        return 400


def call_dict(y):
    print ("The values are ", y["vedu"], y.get("raju"))

"""
connection_string = "mongodb+srv://krisraman:1RyrVRJQCBMIdG77@gemiftcluster.qwn4p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(connection_string)
    db = client.get_database('sample_airbnb')
    user_collection = pymongo.collection.Collection(db, 'gemift_product_db')
    #user_collection.insert_one({"name":"Kris Raman"})
    search_string = '{ "$search": { "index": "gemift_prod_db", "$text": [{ "$query": ["birthday"], "path":"occasion" }] } } '
    #result = user_collection.aggregate([ { "$search": { "index": "gemift_product_db", "$text": [{ "$query": ["birthday"], "path":"occasion" }] }}])
"""

try:
    output_hash = []
    status_code = 0
    #status_code = search_product()
    #status_code = test_get_web_category(3, 10, 20, "F")
    #status_code = test_signup()
    #status_code = test_whatsapp()
    # request_id : 1 --> referring an existing member to an existing friend circle - This will require referrer_user_id, friend_circle_id, friend_user_id
    # request_id : 2 --> referring a non-existing user friend to an existing friend circle - This will require referrer_user_id, friend_circle_id, email_address, name.
    # requests_id : 3 --> creating a friend circle for an existing member as the secret friend - This will require creator_user_id, friend_id, circle name
    # request_id : 4 --> creating a friend circle for a non-existing member as the secret friend - This will require creator_user_id, email_address, name, circle_name
    # request_id : 5 --> a list of friends or contacts from whatsapp to create friend circles.
    #status_code = friend_circle_request_1()
    #status_code = friend_circle_request_2()
    #status_code = friend_circle_request_3()
    #status_code = friend_circle_request_4()
    #status_code = create_occasion()
    #status_code = vote_occasion()
    #status_code = approve_occasion()
    #status_code = get_occasion()
    #status_code = get_friend_circle()
    #status_code = get_friend_circles()
    #status_code = add_interest()
    #status_code = get_interest()
    status_code = search_product_detail()
    #status_code = vote_product()
    #status_code = get_product_votes()
    print ("The status code is", status_code)

except Exception as e:
    print ("The error is ", e)