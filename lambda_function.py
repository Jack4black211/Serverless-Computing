import json 
from pprint import pprint
import boto3


def sendAlertViaSNS(event):
    
    # Create an SNS client using default Session which is instantiated based on the Execution Role assigned to lambda function
    sns_client = boto3.client(service_name="sns", region_name="eu-central-1")
    
    # print(sns_client.check_if_phone_number_is_opted_out(phoneNumber="+XXXXXXXXXXX"))
    # print(dir(sns_client))
    
    # MonthlySpendLimit : maximum amount of money in USD that you are willing to spend per month on sms
    # 'MonthlySpendLimit': '1'
    
    if event['viaSMS']:
        # To set this attribute on all sms sent from AWS SNS service
        response = sns_client.set_sms_attributes(
            attributes={
                # check cloudwatch logs in "eu-central-1"
                'DeliveryStatusIAMRole': 'arn:aws:iam::xx:role/snsCloudWatchLogs',
                'DefaultSenderID': 'EviShopX'
            }
        )
        print('\nsetting sms attributes', response)
    
    
    count_sns_textpublish = 0
    csvData = event['csvRows']
    for row in csvData:
        DueAmount = row['DueAmount']
        DueDate = row['DueDate (dd/mm/yyyy)']
        FirstName = row['FirstName']
        LastName = row['LastName']
        PhoneNum = row['PhoneNum']
        
        # if float(DueAmount) < 1:
        #     # no need to send alert
        #     continue
        
        msg = f"Hi {FirstName},\nPlease pay your due amount={DueAmount} before {DueDate} to avoid extra charges.\nThank you"
        
        # if event['viaEmail']:
            # TODO
        
        if event['viaSMS']:
            print('*** Sending bill due date alert via SMS ***')
            
            #print("DueAmount, DueDate, FirstName, LastName, PhoneNum")
            #print(DueAmount, DueDate, FirstName, LastName, PhoneNum)
            print(msg)
            
            # https://stackoverflow.com/questions/38355151/how-to-send-an-sms-with-custom-sender-id-with-amazon-sns-and-python-and-boto3
            # MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': 'EviShop'},
            #                     'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Promotional'}}
            
            # For testing 
            # https://www.receivesms.com
            
            # Send your sms message.
            sns_client.publish(
                PhoneNumber=PhoneNum,
                Message=msg,
                #MessageAttributes=MessageAttributes    
            )
            
            count_sns_textpublish += 1
        
    return f"EviShopX Bill Payment Alert sent.\nAWS SNS Text Publish triggered for {count_sns_textpublish} rows(s)"



def sendAlertViaTwillio(event):
    from urllib import request, parse
    import base64
    
    # Refrence url
    # https://www.twilio.com/blog/2017/05/send-sms-text-messages-aws-lambda-python-3-6.html
    
    # Evi Twillio Creds
    AccountSid = ""
    Token = ""
    TwillioPhoneNum = ""
    
    # add authentication header to request based on Account SID + Auth Token
    authentication = f"{AccountSid}:{Token}"
    base64string = base64.b64encode(authentication.encode('utf-8'))    

    api_endpoint = f"https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json"
    req = request.Request(api_endpoint)
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
    
    csvData = event['csvRows']
    
    count_twillio_textpublish = 0
    for row in csvData:
        DueAmount = row['DueAmount']
        DueDate = row['DueDate (dd/mm/yyyy)']
        FirstName = row['FirstName']
        LastName = row['LastName']
        PhoneNum = row['PhoneNum']
        
        msg = f"Hi {FirstName},\nPlease pay your due amount={DueAmount} before {DueDate} to avoid extra charges.\nThank you"

        msg_props = {
            "Body":msg,
            "From":TwillioPhoneNum,
            "To": PhoneNum
        }
        
        try:
            # encode the parameters for Python's urllib
            data = parse.urlencode(msg_props).encode()
            print("Sending sms:\n"+msg)
            
            # perform HTTP POST request
            with request.urlopen(req, data) as f:
                print(f"Twilio returned:\n {f.read().decode('utf-8')}")
                count_twillio_textpublish += 1
                
        except Exception as e:
            # something went wrong!
            print(e)
        
        
    return f"EviShopX Bill Payment Alert sent.\nTwillio Text Publish triggered for {count_twillio_textpublish} rows(s)"
    

def lambda_handler(event, context):
    # pprint(event)
    
    alert_status = ""
    
    if event['smsService'] == 'AWS-SNS':
        alert_status = sendAlertViaSNS(event)
        
    elif event['smsService'] == 'Twillio':
        alert_status = sendAlertViaTwillio(event)
        
    else:
        alert_status = "Invalid sms service"
    
    return {
        'statusCode': 200,
        'body': json.dumps(alert_status)
    }
    


