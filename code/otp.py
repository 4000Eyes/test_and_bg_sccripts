from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

VONAGE_API_KEY = "d8b1d37a"
VONAGE_API_SECRET = "Narasimha123@"
VONAGE_BRAND_NAME = "A text message sent using the Vonage SMS API"
TO_NUMBER = "14252815459"

import vonage


def get_code(phone_number):

    response = verify.start_verification(number= phone_number, brand="Gemift")

    if response["status"] == "0":
        print("Started verification request_id is %s" % (response["request_id"]))
    else:
        print("Error: %s" % response["error_text"])

def verify_code(request_id, response_code):


    response = verify.check(request_id, code=response_code)

    if response["status"] == "0":
        print("Verification successful, event_id is %s" % (response["event_id"]))

    else:
        print("Error: %s" % response["error_text"])
        print ("Event id: %s " % response["event_id"])

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
verify = vonage.Verify(client)
value = input("get_code(1), validate_code(2)")
if int(value) == 1:
    phone_number = input("Enter phone number: ")
    get_code(phone_number)
elif int(value) == 2:
    request_id = input("Enter request_id: ")
    code = input("Enter code: ")
    verify_code(request_id, code)