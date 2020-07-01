#
import time
import boto3
from boto3.dynamodb.conditions import Key

millis = int(round(time.time() * 1000))
myTime = time.time()
print(millis)


def query_auctions():
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")

    table = dynamodb.Table('Auctions')
    result = table.query(
      KeyConditionExpression=Key('item_name').eq(item_name)
    )


if __name__ == '__main__':
    item = 'Wise Dragon Helmet'
    auctions_items = query_auctions(item)
    for auction_item in auctions_items:
        print(auction_item['item_name'], ":", auction_item['end'])
