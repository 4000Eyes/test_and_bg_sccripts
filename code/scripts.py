import json

import elasticsearch
from elasticsearch import Elasticsearch

data = {"x":"y", "a":"b"}
d = {"kris":"raman"}

xx = json.dumps(data)
uu = json.loads(xx)

def test(sdic):
    print ("Inside the function", len(sdic))

    for i in sdic.items():
        print ("Item value is ", i[0])
    for i in sdic.keys():
        print ("The dict value is", sdic[i])

print ("The objecct is", xx)

"""
try:
    es = Elasticsearch(
        cloud_id="i-o-optimized-deployment:dXMtd2VzdDEuZ2NwLmNsb3VkLmVzLmlvJDlhMTVkYzcyNDk5OTQwNWQ5MjkzYTIxZTg3Y2MxZTA1JDljMzljZDE5YjA3ZDQ3MmFhODFjNmNhN2ZhNjVmZDJk",
        http_auth=("elastic", "mBbLha3eNawp1emPpYuqSf42"))
except elasticsearch.ElasticsearchException as e:
    print ( e.info)

rs = es.search(index="fte", doc_type='jaiprodrep', body={'query':{'regexp': {'name':'fir*'}}})

print ("The result is", rs)

for row in rs["hits"]["hits"]:
    print ("THe output is", row)
print ("I connected")

"""
li = [1,2,3,4,5,5]

for i in li:
    print ("The value is", i)

dic = {}
dic['re'] = "kris"
dic["v"] = "rama"

print ("The valye of dict is", dic["re"])
print ("The valyee of dict is", dic.get("re"))
test(dic)

def tt(c):
    c.append("test1")
    c.append("test2")

x = []

tt(x)

print ("print", x[0])
print ("print", x[1])



