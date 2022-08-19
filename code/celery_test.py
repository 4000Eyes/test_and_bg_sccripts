"""
import sys
sys.path.insert(0,'/home/krissrinivasan/python/gemiftcelery')
from gemift_celery import add
"""
import json

from celery import Celery


BROKER_URL = 'redis://:rajuvedu123@@localhost:6379/3'
BACKEND_URL = 'redis://:rajuvedu123@@localhost:6379/4'

app = Celery(broker=BROKER_URL )
xstr = json.dumps({"user_id":"XYZ", "first_name":"kris","last_name":"Srinivasan","comm_type":"X", "email_status":"X"})
app.send_task("testing", [xstr])

#print (result.get())

