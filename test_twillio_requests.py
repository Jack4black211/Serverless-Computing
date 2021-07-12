"""
Note:

Directly requests package doen't work on AWS lambda

you need to upload requests package to make it work
"""

import requests
from pprint import pprint

# Evi Twillio Creds
# https://www.twilio.com/console
AccountSid = ""
Token = ""
TwillioPhoneNum = ""


api_endpoint = f"https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json"

msg_props = {
    "Body":"Hello testing twillio-api for Evi",
    "From":TwillioPhoneNum,
    "To": "+15042010052"
}

r = requests.post(url=api_endpoint, auth=requests.auth.HTTPBasicAuth(AccountSid, Token), data=msg_props)

pprint(r.json())





"""*********************************************
Demo of recieving message on ""
https://www.receivesms.co/us-phone-number/3446/

*********************************************"""


"""*********************************************
REFERENCE links

https://www.twilio.com/docs/sms/api/message-resource

for trial account every To recipient number needs to be added first
https://www.twilio.com/console/phone-numbers/verified

also make sure you have geo permission to send sms from your twillio number
https://www.twilio.com/console/sms/settings/geo-permissions

*********************************************"""


"""*********************************************
Possible Errors

Trial Account unverified To number
https://www.twilio.com/docs/errors/21608

Geo Permission
https://www.twilio.com/docs/api/errors/21408

*********************************************"""