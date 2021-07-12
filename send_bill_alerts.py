"""
Author: Ev4stef

Project: Serverless Computing

Description: We are using AWS Servless service like lambda, SNS (Text messaging)
             In addition to these we are using API Gateway, CloudWatch

             This script takes .csv file as input and send invocation call to lambda function through rest-api
             and prints the response of lambda function execution.
"""

# Python already have these packages preinstalled so no need to install them
import csv
import sys
from pprint import pprint as pp


# External Packages, Needs to be installed for example using pip
# If these packages are not install program will not work

# USE pip commands to install packages

# pip install requests
# pip install tkinter

try:
    # to show csv row data in table
    from prettytable.prettytable import PrettyTable
    # to send request AWS gateway API
    import requests
    # to show file explorer GUI
    from tkinter import Tk, filedialog 

except Exception as e:
    print('Please make sure that all the External Packages are installed properly.')
    print(e)
    sys.exit()

# To open file explorer without background window
# https://stackoverflow.com/questions/35384011/is-there-a-way-to-remove-the-background-window-that-pops-up-when-calling-askopen

Tk().withdraw()

program_info = "EviShopX - Send bill due date alert using AWS Serverless Services\nPowered by AWS-Lambda, AWS-SNS, Twillio REST-API\n"
print(program_info)

field_names = ["PhoneNum","FirstName","LastName","DueAmount","DueDate (dd/mm/yyyy)"]
instruction = f"Please select a .csv file which contains Customer-Bill-Data when file explorer pops.\nCSV file should contain following fields:-\n{field_names}"

print(instruction,end='\n')

validDataTable = PrettyTable()
validDataTable.field_names = field_names

invalidDataTable = PrettyTable()
invalidDataTable.field_names = field_names

csvFileName =""
while True:
    # show file explorer so that user can select .csv file
    csvFileName = filedialog.askopenfilename(title="Please select a .csv file which contains Customer-Bill-Data", filetypes=[("CSV file", "*.csv")])
    
    if csvFileName.lower().endswith(".csv"):
        # user has selected a .csv file we can exit from this while loop
        print(f"\n\nYour selected filepath: {csvFileName}\n\n")
        break
    else:
        ans = input('do you want to select .csv file? y/n :')
        if ans != "" and ans[0].lower() == 'y':
            # while loop will run
            continue
        else:
            print("You didn't select any file.\nExiting...")
            sys.exit()

selected_service = ""

# SNS - Simple Notification Service

choice = {
    "1" : "AWS-SNS",
    "2" : "Twillio"
}

while True:
    # price of sms through aws changes
    service_id = input(f"Select Text Messaging serivce to be used by AWS lambda\npress 1: AWS-SNS (Note: It's not Free charges approx $0.08)\npress 2: Twillio\n>")
    try:
        selected_service = choice[service_id]
        print('\nDue Bill Payment Alert will be sent using: ',selected_service)
        break

    except KeyError as e:
        #print(e)
        print("\nTry Again! Please enter 1 or 2 depending on your choice")


csvData = []
cnt_valid_rows, cnt_invalid_rows = 0, 0

with open(csvFileName, newline='') as csvFile:
    csvReader = csv.DictReader(csvFile, delimiter=',')
    for row in csvReader:
        # row is a dictionay = { "PhoneNum":"", "FirstName":"Tommy"..}
        # pp(row)

        row_values = [row["PhoneNum"],row["FirstName"],row["LastName"],row["DueAmount"],row["DueDate (dd/mm/yyyy)"]]
        
        # if any of the value gives False then it's a Invalid row
        values_status = [True if val != None and val.strip() != "" else False for val in row_values]

        # all [True,True,True,True,True] --> Valid row

        if all(values_status):
            # all the values are non-empty in row
            # so it's a valid row
            validDataTable.add_row(row_values)
            csvData.append(row)
            cnt_valid_rows += 1
        else:
            # INVALID
            invalidDataTable.add_row(row_values)
            cnt_invalid_rows += 1

print("Sending request to AWS API to Trigger lambda function: sendBillPaymentAlert, for following customers:-")
print(validDataTable,end='\n\n')

if cnt_invalid_rows > 0:
    print(f"Please check {csvFileName}\nIt contains {cnt_invalid_rows} row(s) which doesn't have value for all the fields:\n{field_names}")
    print(invalidDataTable,end='\n\n')



if input("press i to To invoke lambda function: sendBillPaymentAlert\nor any other key to stop program: ").lower() == "i":
    
    # Don't Share this API_ENDPOINT with anyone as it's not secured with token, api-key or anything

    API_ENDPOINT = "xxx/dev/sendBillPaymentAlert"
    r = requests.post(url = API_ENDPOINT, json = {'csvRows' : csvData, 'smsService':selected_service, 'viaSMS': True, 'viaEmail': False})

    print('\nResponse of invoking sendBillPaymentAlert lambda function')
    pp(r.json())

    print('_'*100)
    input('\nThank you for using, press any key to exit.')

else:
    sys.exit()



"""
https://www.receivesms.co/us-phone-number/3446/

"""



"""

AWS SNS - SUCCESS

{
    "notification": {
        "messageId": "x",
        "timestamp": "2020-12-28 20:32:10.932"
    },
    "delivery": {
        "phoneCarrier": "x",
        "mnc": 1,
        "numberOfMessageParts": 1,
        "destination": "",
        "priceInUSD": 0.08621,
        "smsType": "Promotional",
        "mcc": 202,
        "providerResponse": "Message has been accepted by phone",
        "dwellTimeMs": 525,
        "dwellTimeMsUntilDeviceAck": 3447
    },
    "status": "SUCCESS"
}

"""