from __future__ import print_function # Python 2/3 compatibility 
import boto3 
import json 
import decimal 
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

table = dynamodb.Table('Movies')

print("Movies from 1985")

response = table.query(
    KeyConditionExpression=Key('year').eq(1985)
)

for i in response['Items']:
    print(i['year'], ":", i['title'])

