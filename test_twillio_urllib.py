import base64
from urllib import request, parse

# Refrence url
# https://www.twilio.com/blog/2017/05/send-sms-text-messages-aws-lambda-python-3-6.html

# Evi Twillio Creds
AccountSid = ""
Token = ""
TwillioPhoneNum = ""

api_endpoint = f"https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json"

msg_props = {
    "Body":"Hello testing twillio-api for Evi urllib",
    "From":TwillioPhoneNum,
    "To": ""
}


# encode the parameters for Python's urllib
data = parse.urlencode(msg_props).encode()
req = request.Request(api_endpoint)

# add authentication header to request based on Account SID + Auth Token
authentication = f"{AccountSid}:{Token}"
base64string = base64.b64encode(authentication.encode('utf-8'))
print("Authorization", "Basic %s" % base64string.decode('ascii'))


req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))

try:
    # perform HTTP POST request
    with request.urlopen(req, data) as f:
        print(f"Twilio returned:\n {f.read().decode('utf-8')}")
except Exception as e:
    # something went wrong!
    print(e)

