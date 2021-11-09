import elasticsearch
from elasticsearch import Elasticsearch, helpers
import json

class FTESearch:
    def __init__(self):
        self._es = None
        self._index = None

    def _set_index(self, index):
        self._index = index

    def _connect_search(self):
        try:
            self._es = Elasticsearch(cloud_id="i-o-optimized-deployment:dXMtd2VzdDEuZ2NwLmNsb3VkLmVzLmlvJDlhMTVkYzcyNDk5OTQwNWQ5MjkzYTIxZTg3Y2MxZTA1JDljMzljZDE5YjA3ZDQ3MmFhODFjNmNhN2ZhNjVmZDJk",
                       http_auth=("elastic", "mBbLha3eNawp1emPpYuqSf42"))
        except elasticsearch.ElasticsearchException as e:
                print ("The error is", e.info)
                return None
    def insert_item(self, data):
        try:
        # index and doc_type you can customize by yourself
            res = self._es.index(index=self._index, doc_type='jaiprodrep', id=5, body=data)
            # index will return insert info: like as created is True or False
            print(res)
            return res

        except elasticsearch.ElasticsearchException as e:
            print("The error is", e.info)
            return None
        except:
            return None

    def full_text_search(self, keyword, field):
        try:
            res = self._es.search(
            index=self._index,body={"query":{"match": { field: keyword}}})
            print ("The results is", res)
            return res
        except elasticsearch.ElasticsearchException as e:
            return None
        except:
            return None
    def regex_search(self, pat, field):
        try:
            res = self._es.search(
                index=self._index,
                body={ "query":{ "wildcard": { field: pat}}})
            print ("The regex", res)
            return res
        except elasticsearch.ElasticsearchException as e:
            print (e.info)
            return None
        except:
            print ("Unexplained Error")
            return None


    def select_filter_sort(self, lquery_key, lquery_value, lfilter_key, lfilter_value, lsort_key, lsort_value, lsort_dt_key):
        try:
            res = self._es.search(
                index=self._index,
                body = {"query": {
                "bool": {
                    "must": {
                        "match": {
                            lquery_string
                                }
                            },
                    "filter": [
                            lfilter_string
                            ]
                        ,
                    "sort": [
                        lsort_string
                        ]
                    }
                    }
                })

            print ("The regex", res)
            return res
        except elasticsearch.ElasticsearchException as e:
            print (e.info)
            return None
        except:
            print ("Unexplained Error")
            return None




    data = '{"index":"fte","product_id":"12212",' \
'"product name": "Pasaroduct Name 1", "product_desc": ' \
'"THis is the description of product 1", "Location Id": ["IND"], "User_Age_Lo": "2", "User_Ager_Hi": "10", ' \
'"Category": ["sports", "cricket", "chennai"], "Relevance Age Group": "2-10", "Gender":"Male", "Seasonality": ' \
'"Yes"' \
'}'

print (data)

objClass = FTESearch()
objClass._set_index("fte")
objClass._connect_search()
#objClass.insert_item(data)
objClass.full_text_search("sports", "category")
objClass.full_text_search("IND", "location id")
objClass.regex_search("this", "Product Desc")
print ("Successful!")

