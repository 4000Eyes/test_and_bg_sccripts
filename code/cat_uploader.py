from csv import reader
import requests
import json

flag = 0
request_id = 0
merch_hash = {}
web_category_hash = {}
web_subcategory_hash = {}
brand_hash = {}
merch_web_hash = {}
web_sub_hash = {}
sub_brand_hash = {}

def insert_entities(request_id, value, description, age_lo, age_hi, gender):
    parameters = {
        "request_id": request_id,
        "value": value,
        "description": description,
        "age_lo":age_lo,
        "age_hi":age_hi,
        "gender":gender
    }
    response = requests.post("http://localhost:5000/api/category", json=parameters)
    print("The status code is", response.status_code)
    return response.json()

def insert_relationship(request_id, key1, value1, key2, value2):
    try:
        print ("The arguements are ", request_id, key1, key2, value1, value2)
        parameters = {
            "request_id": request_id,
            key1 : value1,
            key2 : value2
        }
        response = requests.post("http://localhost:5000/api/category", json=parameters)
        print("The status code for relationshup is", response.status_code, parameters)
        return response.status_code
    except Exception as e:
        print ("There is an exception with the request")
        return 400

with open('/home/krissrinivasan/cathierarchy', 'r') as read_obj:
    lines = read_obj.readlines()
    for line in lines:
        line = line.strip()
        line = line.rstrip('\n')
        line = line.rstrip('\t')
        if len(line) > 0:
            if line == "Merch Categories:":
                request_id = 1
            elif line == "Web Categories:":
                request_id = 2
            elif line == "Sub Categories:":
                request_id = 3
            elif line == "Brands:":
                request_id = 4
            elif line == "Merch-Web:":
                request_id = 7
            elif line == "Web-Sub:":
                request_id = 5
            elif line == "Sub-brand:":
                request_id = 6
                print("Not ready for split")
            else:
                val = line.split('|')
                print ('Number of fields ', len(val))
                if len(val) == 5:
                    print("The line is ", val[0], val[1], val[2], val[3], val[4])
                    val[0] = val[0].strip()
                    val[1] = val[1].strip()
                    val[2] = val[2].strip()
                    val[3] = val[3].strip()
                    val[4] = val[4].strip()
                else:
                    print("The line is ", val[0], val[1])
                    val[0] = val[0].strip()
                    val[1] = val[1].strip()


                return_code = 0
                if request_id == 7:
                    print ("The merch hash is", web_category_hash)
                    merch_category_id = merch_hash.get(val[0])
                    web_category_id = web_category_hash.get(val[1])
                    return_code = insert_relationship(request_id, "merch_category_id", merch_category_id, "web_category_id", web_category_id)
                    if return_code != 200:
                        print ("Error in insert merch web relation for ", merch_category_id, web_category_id)
                        exit(0)
                    print ("The combination of merch and web category is ", merch_category_id, web_category_id)
                if request_id == 5:
                    web_category_id = web_category_hash.get(val[0])
                    web_subcategory_id = web_subcategory_hash.get(val[1])
                    print("The category hash is ", web_category_hash)
                    print ("The file values are ", val[0], val[1])
                    return_code = insert_relationship(request_id, "web_category_id", web_category_id, "web_subcategory_id", web_subcategory_id)
                    if return_code != 200:
                        print ("Error in inserting web sub relation for ", web_category_id, web_subcategory_id)
                        exit(0)
                    print ("The combination of web category and web subcategory is ", web_category_id, web_subcategory_id)
                if request_id == 6:
                    web_subcategory_id = web_subcategory_hash.get(val[0])
                    brand_id = brand_hash.get(val[1])
                    return_code = insert_relationship(request_id, "web_subcategory_id", web_subcategory_id,  "brand_id", brand_id)
                    if return_code != 200:
                        print ("Error in inserting sub brand relationship for ", web_subcategory_id, brand_id)
                        exit(0)
                    print ("The combinations of web_subcategory and brand is", web_subcategory_id, brand_id)


                if request_id == 1:
                    output = insert_entities(request_id, val[0], val[1], val[2], val[3], val[4])
                    merch_hash[val[0]] = output["merch_category_id"]
                    print ("The merch category id is ", merch_hash[val[0]])
                if request_id == 2:
                    output = insert_entities(request_id, val[0], val[1], val[2], val[3], val[4])
                    web_category_hash[val[0]] = output["web_category_id"]
                    print ("The web category id is ", web_category_hash[val[0]])
                if request_id == 3:
                    output = insert_entities(request_id, val[0], val[1], val[2], val[3], val[4])
                    web_subcategory_hash[val[0]] = output["web_subcategory_id"]
                    print ("The web subcategory id is ", web_subcategory_hash[val[0]])
                if request_id == 4:
                    output = insert_entities(request_id, val[0], val[1], val[2], val[3], val[4])
                    brand_hash[val[0]] = output["brand_id"]
                    print ("The  brand id is ", brand_hash[val[0]])

    exit(0)


