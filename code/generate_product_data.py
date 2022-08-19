import json
import random
from pymongo import errors, MongoClient
import pymongo.collection
import os
data = {}

product_id = 10000
product_description = "This is test data generated for gemift.com. The product id is "
product_title = "This is product title"

def load_interest_data(hshinterests, linterests):
    try:
        client = MongoClient(db_string)
        result = []
        x = client.get_database("sample_airbnb")
        email_collection = pymongo.collection.Collection(x, "interests")
        result = email_collection.find()
        for row in result:
            hshinterests[row["interest_id"]] = row["interest_name"]
            linterests.append(row["interest_id"])
        return result
    except Exception as e:
        print("The generic error is", e)
        return None

code_environment = os.environ.get("BG_ENVIRON")
if code_environment == "test":
    db_string = os.environ.get("MONGO_TEST")
"""
interest = ["138345a7-419a-44dd-ac2f-a6017991902c","4b85d7ec-8dac-4b0f-b131-4ee79858e4bc","13fdf6ac-3dcd-4aaa-aee4-0e6f5d2455f3",
"d4400278-40e3-4b0d-81ff-d4f0c3a05757",
    "42f4d0d3-117e-49ff-85ec-8e5e0738a006",
"c45cb0cd-496a-46aa-9a77-21f95d623780",
"db50e7b7-0865-43e8-b54f-82c5aea0da5a",
"7c06a01a-a10e-4e46-b2a4-0a471a11da07",
"74954898-edb4-4e61-b866-77ab927a7414",
"98c08b50-56cc-4594-ba12-7b97f1be4d22",
"7331c93b-e4ec-4307-9dac-cba4dbedd023",
"960055ed-073c-412a-9360-ac5054f28984",
"5abefaf0-8db2-47ba-b8d2-6ea391a6708a",
"0e3f1bc1-f58c-42c7-af18-c7bfc846e1d9",
"b3af3682-8db4-443b-99dd-706403a243c3"

]
cat_name = {"A121": "Electronics","A122":"Home","A123":"Software","A124":"Test2","A125":"Travel","A126":"Hobby","A127":"Running","A128":"Utensils","A129":"Sports","A130":"Outdoors","A131":"Entertainment"}
interest_name = {"138345a7-419a-44dd-ac2f-a6017991902c":"All Kinds of Phones",
               "4b85d7ec-8dac-4b0f-b131-4ee79858e4bc":"Head phone or ear phones",
                "69cf47dd-3eeb-4449-a7c9-1407a21a1b9c":"Music Instruments",
"13fdf6ac-3dcd-4aaa-aee4-0e6f5d2455f3":"Techno Instruments",
"d4400278-40e3-4b0d-81ff-d4f0c3a05757":"Video games Obsession",
"42f4d0d3-117e-49ff-85ec-8e5e0738a006":"Fall for Apple gears",
 "c45cb0cd-496a-46aa-9a77-21f95d623780":"Fall for Samsung gears",
"db50e7b7-0865-43e8-b54f-82c5aea0da5a":"Give me smart Wearables",
"7c06a01a-a10e-4e46-b2a4-0a471a11da07":"Samsung appliances lover",
               "74954898-edb4-4e61-b866-77ab927a7414":"Apple Fan boy",
"98c08b50-56cc-4594-ba12-7b97f1be4d22":"Loves keyboards",
"7331c93b-e4ec-4307-9dac-cba4dbedd023":"Loves beaches",
"960055ed-073c-412a-9360-ac5054f28984":"Thai food lover",
"5abefaf0-8db2-47ba-b8d2-6ea391a6708a":"ANything meat",
"0e3f1bc1-f58c-42c7-af18-c7bfc846e1d9":"Loves Kerala - God's country",
"b3af3682-8db4-443b-99dd-706403a243c3":"Loves walking"
}
"""
hshinterests = {}
linterests = []

load_interest_data(hshinterests, linterests)
price = [10.02,20.02,30.03,40.03,50.09,60.09,80.90, 120.20, 140.08, 200.00]
age_range_list = [[0,5],[6,10,],[11,15], [15,19], [20,30], [31,39], [40,49], [50,60], [60,100],[101,150]]
gender_list = ["M","F","A"]
website_url = ["http://www.amazon.com","http://www.flipkart.com","http:///www.ebay.com","http:///www.dealshare.in"]
occasion = [["Birthday","GEM-OCC-999999"], ["Valentines Day","2"],["Wedding Anniversary","GEM-OCC-000124"],["Met my girlfriend","GEM-OCC-000125"],["Mothers day","5"],["Fathers Day","6"]]
season_product = ["Y","N"]
country = ["India","Europe","USA","Singapore","Hong Kong","Malaysia","Thailand", "All"]

file_handle = open("/home/krissrinivasan/Downloads/product_gemift.json","w")
for occasion_row in occasion:
    for interest_id in linterests:
        for i in range(1,200):
            data = {}
            product_id = product_id + 1
            data["product_id"] = product_id
            data["product_title"] = product_title + " " + str(product_id)
            data["product_description"] = product_description + str(product_id)
            data["interest"] = interest_id
            data["interest_name"] = hshinterests[interest_id]
            data["price"] = random.choice(price)
            data["gender"] = random.choice(gender_list)
            age_range = random.choice(age_range_list)
            data["age_lo"] = age_range[0]
            data["age_hi"] = age_range[1]
            data["website_url"] = random.choice(website_url)
            data["seasonal_product"] = random.choice(season_product)
            data["occasion_name"] = occasion_row[0]
            data["occasion_id"] = occasion_row[1]
            data["country"] = random.choice(country)

            json_data = json.dumps(data)

            file_handle.write(json_data + "\n")

            print ("Json data ", json_data)

