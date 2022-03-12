import json

f = open("/home/krissrinivasan/Downloads/meta.json")

data = json.load(f)

for row in data["xt"]:
    print ("The json is ", row["name"])