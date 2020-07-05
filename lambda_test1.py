# skeleton script for retrieving items that expire within a certain timeframe, default 15 minutes
import time
import boto3
import json
from boto3.dynamodb.conditions import Key

time_in_milli = int(round(time.time() * 1000))
myTime = time.time()
print(time_in_milli)
minutes_to_monitor = 15
monitor_time = time_in_milli + minutes_to_monitor * 60 * 1000
# monitor_time = 1593413148482 ; testing
print(monitor_time)

def query_auctions(item_name):
    # if not dynamodb:
    dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")

    table = dynamodb.Table('Auctions')
    result = table.query(
      KeyConditionExpression=Key('item_name').eq(item_name)
    )
    return result['Items'] # Need to return the correct Items from the table ...

def lambda_handler(event, context):
    # Go
    response = {}
    item_name = 'Wise Dragon Helmet' # This variable needs to be an option to the user
    auctions_items = query_auctions(item_name)
    counter = 1
    ## calculate how long until item expires ... expires_at = ; and include in the response
    for auction_item in auctions_items:
        if auction_item['end'] <= monitor_time:
            print(auction_item['item_name'], ":", auction_item['end'], ":", auction_item['starting_bid'], ":", auction_item['highest_bid_amount'])
            myKey = auction_item['item_name'] +  auction_item['end']
            myValue = auction_item['highest_bid_amount']
            response = response.update({myKey : myValue})

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

if __name__ == '__main__':
    ## item_name = 'Wise Dragon Helmet' # This variable needs to be an option to the user
    ## auctions_items = query_auctions(item_name)
    lambda_handler(event, {}) # event ... ?
    ## for auction_item in auctions_items:
    ##     if auction_item['end'] <= monitor_time:
    ##         print(auction_item['item_name'], ":", auction_item['end'], ":", auction_item['starting_bid'], ":", auction_item['highest_bid_amount'])
