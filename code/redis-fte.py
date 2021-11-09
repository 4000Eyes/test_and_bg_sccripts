import json
from datetime import datetime
import redis
import json
r = redis.Redis(
    host = "127.0.0.1",
    port = 6379,
    password="rajuvedu123@"
)

dict = {"a" :1, "b": 2}
rval = json.dumps(dict)
dict["c"] = 34

bb = dict.get("c")

print ("The value of b", bb)
r.set("kk", rval)

y = r.get("kk")

print ("The value is", json.loads(y))

r.lpush('k123', 1,34,3)

x = r.lrange('k123', 0,2)

x = r.lpop('k123')

print (x)

a = {"a":1, "b":2}
b = {"a":1, "c":3}

c = {**a, **b}

a.update(b)

print ("The merrged" , a)

x = [1,2,3,4]

for i in x:
    print ("The initial values is", i)
    for c in x:
        if i != c :
            print ("The list value is", c)

user = [{"name": "kris", "age":45}, {"name":"vidya", "age": 40}]

#for row in user:
#   print ("Name", row["name"])

dttime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

print ("date time is", dttime)