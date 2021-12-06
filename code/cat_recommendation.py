import numpy as py
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import pickle
import neo4j.exceptions
from neo4j import GraphDatabase
from pymongo import errors, MongoClient
import pymongo.collection

def connect_to_graph():
    try:
        driver = GraphDatabase.driver(os.environ.get("FTEYES_GDB_URI"), auth=(os.environ.get("FTEYES_GDB_USER"), os.environ.get("FTEYES_GDB_PWD")))
        return driver
    except neo4j.exceptions.Neo4jError as e:
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


def extract_subcategory_data(age_lo, list_output=[]):

    query = "MATCH (a:WebSubCategory)-[r:INTEREST]->() " \
            " WHERE age_lo = $age_lo_" \
            " RETURN r.friend_circle_id, a.web_subcategory_id,  1 as value " \
            " ORDER BY age_lo"
    g_db_handle = connect_to_graph()
    result = g_db_handle.run(query, age_lo_ = age_lo)
    for record in result:
        list_output.append(record.data())
    return True


def run_mb_algo(loutput, model_output_file_name):

    mb_df = pd.DataFrame(loutput).fillna(0)
    mba_model = apriori(mb_df, min_support=0.07, use_colnames=True)
    with open(model_output_file_name, 'wb') as f:
        pickle.dumps(mba_model, f)
        f.close()

    my_rules = association_rules(mba_model, metric="confidence", min_threshold=1)
    return True






#converting all positive vaues to 1 and everything else to 0

hshInterest = [
    {"friend_circle_id" : "23231212", "love nature" : 1, "love tea" : 1 },
    {"friend_circle_id": "23231212", "love x": 1, "love tea": 1},
    {"friend_circle_id": "23231212", "love y": 1, "love r": 1},
    {"friend_circle_id": "23231212", "love nature": 1, "love tea": 1, "love c": 1},
    {"friend_circle_id": "23231212", "love x": 1, "love b": 1},
    {"friend_circle_id": "23231212", "love nature": 1, "love e": 1, "love f" : 1},
    {"friend_circle_id": "23231212", "love a": 1, "love tea": 1, "love c" : 1},
    {"friend_circle_id": "23231212", "love nature": 1, "love b": 1, "love f" : 1}
]
"""
def my_encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


myretaildata = pd.read_excel('/home/krissrinivasan/Downloads/retail.xlsx')

myretaildata['Description'] = myretaildata['Description'].str.strip() #removes spaces from beginning and end
myretaildata.dropna(axis=0, subset=['InvoiceNo'], inplace=True) #removes duplicate invoice
myretaildata['InvoiceNo'] = myretaildata['InvoiceNo'].astype('str') #converting invoice number to be string
myretaildata = myretaildata[~myretaildata['InvoiceNo'].str.contains('C')] #remove the credit transactions

mybasket = (myretaildata[myretaildata['Country'] =="Germany"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)  
          .set_index('InvoiceNo'))

my_basket_sets = mybasket.applymap(my_encode_units)
my_basket_sets.drop('POSTAGE', inplace=True, axis=1) #Remove "postage" as an item

my_frequent_itemsets = apriori(my_basket_sets, min_support=0.07, use_colnames=True)

my_rules = association_rules(my_frequent_itemsets, metric="confidence", min_threshold=1)


print (my_rules.head(20))

"""