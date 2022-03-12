import json
from os import listdir
import os
import neo4j.exceptions
from neo4j import GraphDatabase

def connect_to_graph():
    try:
        driver = GraphDatabase.driver(os.environ.get("FTEYES_GDB_URI"), auth=(os.environ.get("FTEYES_GDB_USER"), os.environ.get("FTEYES_GDB_PWD")))
        return driver
    except neo4j.exceptions.Neo4jError as e:
        return None

def load_occasion(db_handle, data, key):

    query = "merge (a:occasion{occasion_id:$occasion_id_}) " \
            " on match set a.status_id= $status_," \
            "a.friend_circle_id = null " \
            " on create set a.occasion_name = $occasion_name_, " \
            " a.occasion_frequency = $occasion_frequency_," \
            " a.status_id = $status_," \
            "a.friend_circle_id = null"
    try:
        driver = db_handle.session()
        txn = driver.begin_transaction()
        for row in data[key]:
            result = txn.run(query, occasion_id_ = row["occasion_id"],
                                occasion_name_ = row["occasion_name"],
                                occasion_frequency_ = row["occasion_frequency"],
                                status_ = int(row["status"]))
        txn.commit()
    except neo4j.exceptions.Neo4jError as e:
        txn.rollback()
        print("The error is", e)
        return False

def load_category(db_handle, data, key):

    query = "merge (a:WebCat{web_category_id:$web_category_id_}) " \
            " on match set a.web_category_name=$web_category_name_ " \
            " on create set a.web_category_id = $web_category_id_, " \
            " a.web_category_name = $web_category_name_"
    try:
        driver = db_handle.session()
        txn = driver.begin_transaction()
        for row in data[key]:
            result = txn.run(query, web_category_id_ = row["web_category_id"],
                                web_category_name_ = row["web_category_name"])
        txn.commit()
    except neo4j.exceptions.Neo4jError as e:
        txn.rollback()
        print("The error is", e)
        return False


def load_subcategory(db_handle, data, key):

    query = "merge (a:WebSubCat{web_subcategory_id:$web_subcategory_id_}) " \
            " on match set a.web_subcategory_name=$web_subcategory_name_ ," \
            "a.parent_id = $parent_id_, a.age_lo = $age_lo_, a.age_hi= $age_hi_" \
            " on create set a.web_subcategory_id = $web_subcategory_id_, " \
            " a.web_subcategory_name = $web_subcategory_name_ ," \
            " a.parent_id = $parent_id_, a.age_lo = $age_lo_, a.age_hi= $age_hi_"
    try:
        driver = db_handle.session()
        txn = driver.begin_transaction()
        for row in data[key]:
            result = txn.run(query, web_subcategory_id_ = row["web_subcategory_id"],
                                web_subcategory_name_ = row["web_subcategory_name"],
                                parent_id_ = row["parent_id"],
                                age_lo_ = row["age_lo"],
                                age_hi_ = row["age_hi"])
        txn.commit()
    except neo4j.exceptions.Neo4jError as e:
        txn.rollback()
        print("The error is", e)
        return False

def load_brand(db_handle, data, key):

    query = "merge (a:brand{brand_id:$brand_id_}) " \
            " on match set a.brand_name=$brand_name_ " \
            " on create set a.brand_id = $brand_id_, " \
            " a.brand_name = $brand_name_"
    try:
        driver = db_handle.session()
        txn = driver.begin_transaction()
        for row in data[key]:
            result = txn.run(query, brand_id_ = row["brand_id"],
                                brand_name_ = row["brand_name"])
        txn.commit()
    except neo4j.exceptions.Neo4jError as e:
        txn.rollback()
        print("The error is", e)
        return False

def load_brand_subcategory(db_handle, data, key):

    # query = "merge (a:brand_subcategory{brand_id:$brand_id_, web_subcategory_id:$web_subcategory_id_}) " \
    #         " on match set a.status=$status_ " \
    #         " on create set a.brand_id = $brand_id_, " \
    #         " a.web_subcategory_id = $web_subcategory_id_," \
    #         " a.status = $status_"
    query = "match (a:brand{brand_id:$brand_id_}), (ws:WebSubCat{web_subcategory_id:$web_subcategory_id_}) " \
              " merge (a)-[r:BRAND]->(ws) " \
              " on create set r.status = $status_ " \
              " on match set r.status = $status_ " \
            " return a.brand_id"
    try:
        driver = db_handle.session()
        txn = driver.begin_transaction()
        for row in data[key]:
            result = txn.run(query, brand_id_ = row["brand_id"],
                                web_subcategory_id_ = row["web_subcategory_id"],
                                status_ = row["status"])
        txn.commit()
    except neo4j.exceptions.Neo4jError as e:
        txn.rollback()
        print("The error is", e)
        return False


db_handle = connect_to_graph()

file_name = "/home/krissrinivasan/Downloads/json/"


files_to_ingest = ["occasion.json","brand.json", "category.json","subcategory.json","brand-subcategory.json"]

for file in files_to_ingest:
    f = open(file_name + file)
    data = json.load(f)

    for key in data:
        if key == "category_data":
            load_category(db_handle, data, "category_data")
        if key == "brand_data":
            load_brand(db_handle, data,"brand_data")
        if key == "subcategory_data":
            load_subcategory(db_handle, data,"subcategory_data")
        if key == "brand_subcategory_data":
            load_brand_subcategory(db_handle,data,"brand_subcategory_data")
        if key == "occasion_data":
            load_occasion(db_handle, data, "occasion_data")

    f.close()


