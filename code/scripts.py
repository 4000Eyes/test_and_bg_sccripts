import json

import elasticsearch
from elasticsearch import Elasticsearch
import pytz
from datetime import datetime, tzinfo, timedelta


def get_age_range( val, rhsh):
    range_list = [[0, 5], [6, 10, ], [11, 15], [15, 19], [20, 30], [31,39], [40 , 49], [50 ,60], [60 ,100]]
    for i in range_list:
        r = range(i[0], i[1])
        if val in r:
            rhsh["lo"] = i[0]
            rhsh["hi"] = i[1]
            return True
    return False

hsh = {}
b = get_age_range(23,hsh)
print ("The low and high are ", hsh["lo"], hsh["hi"])

sample_dt = "30-11-2021"
dobject = datetime.strptime(sample_dt, "%d-%m-%Y" )
utc_val = dobject.astimezone(tz=pytz.UTC)
east_val = utc_val.astimezone((pytz.timezone('US/Eastern')))
fmx = datetime.strftime(east_val, "%d-%m")

print (pytz.all_timezones)


utc_now_dt = datetime.now(tz=pytz.UTC)
formatted_datetime = utc_now_dt.strftime("%d-%m-%Y %H-%M-%S")
x = datetime.strptime(formatted_datetime, "%d-%m-%Y %H-%M-%S" )
y = x + timedelta(days=3)
print('Current Datetime in UTC: ', utc_now_dt, formatted_datetime, y, dobject)
print ("utc_val, east_val", utc_val, east_val)

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
