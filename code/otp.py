import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

VONAGE_API_KEY = "d8b1d37a"
VONAGE_API_SECRET = "YaYRHm0vEwfFRdeE"
VONAGE_BRAND_NAME = "A text message sent using the Vonage SMS API"
TO_NUMBER = "14252815459"

import vonage

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
verify = vonage.Verify(client)

response = verify.start_verification(number= TO_NUMBER, brand="AcmeInc")

if response["status"] == "0":
    print("Started verification request_id is %s" % (response["request_id"]))
else:
    print("Error: %s" % response["error_text"])