from __future__ import print_function
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import requests
from pprint import pprint

# Types of emails
# Registration thank you email
# Registration confirmation email
# Invitation email
# Forgot password email
# Reminder about Invitation email
# Product email


class EmailManagement():

    def __init__(self):
        self.configuration = None
    # Configure API key authorization: api-key
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = os.environ.get('EMAIL_SERVICE_API_KEY')

    def send_email(self, template_id):
        subject = "My Subject"
        # Uncomment below lines to configure API key authorization using: partner-key
        # configuration = sib_api_v3_sdk.Configuration()
        # configuration.api_key['partner-key'] = 'YOUR_API_KEY'

        # create an instance of the API class
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email":"krishnan@gemift.com","name":"Kris Srinivasan"}], template_id=template_id, params={"GEM_NAME": "Kris Srinivasan","FIRSTNAME": "Rama"}, headers={"Content-Type":"application/json", "accept":"application/json", "charset": "iso-8859-1"}) # SendSmtpEmail | Values to send a transactional email

        try:
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

    def create_contact(self, email, first_name, last_name):
        api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(self.configuration))

        create_contact = sib_api_v3_sdk.CreateContact(email=email, update_enabled=True,
                                                      attributes={'FIRSTNAME': first_name, 'LASTNAME': last_name}, list_ids=[1])

        try:
            api_response = api_instance.create_contact(create_contact)
            print(api_response)
        except ApiException as e:
            print("Exception when calling ContactsApi->create_contact: %s\n" % e)



objEmail = EmailManagement()

objEmail.create_contact("rajuvedu1029@gmail.com", "Raju", "Vedu")
print ("Successfully added")