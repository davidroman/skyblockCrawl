
import requests
import json
import sys
import datetime
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Auctions')

APIKEY = sys.argv[1]
# text = sys.argv[2]

def skyblockAuction(myAPIKey, i):
    print('call Skyblock auction API');
    page = str(i)
    base_url='https://api.hypixel.net/skyblock/auctions'
    URL=base_url + "?page=" + page + "&key=" + myAPIKey
    try:
        response = requests.get(URL)
    except ValueError as e:
        print(e)

    try:
        myData = response.json();
    except ValueError as e:
        print(e)

    return myData

# write data to my file
def writeData(data):
    with open('skyblockAuctions.json', 'a+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# insert data into DynamoDb
def insertDynamodb(data):
    myAuctions = data['auctions']
    with table.batch_writer() as batch:
        for auction in myAuctions:
            batch.put_item(Item=auction)

## def maybeInsertDynamodb(data):
##     dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
##     table = dynamodb.Table('Auctions')
##     myAuctions = data['auctions']
##     for auction in auctions:
##         table.put_item(Item=auction)


for i in range(30):
    data = skyblockAuction(APIKEY, i)
    writeData(data)
    insertDynamodb(data)


# data = skyblockAuction(APIKEY)
