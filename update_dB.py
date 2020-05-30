#*** PROGRAM : update_dB.py
#*** DESCRIPTION : Insert data serires in DataSeries, in DynamoDB
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+AF
#*** VERSION: 1.1 DATE: 202005301845 AUTHOR: MC
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments

from __future__ import print_function
import boto3
import decimal
import json
from datetime import datetime


from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def update_dB(last_time_dB):

    class DecimalEncoder(json.JSONEncoder):
        def default(self,o):
            if isinstance(o,decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('DataSeries')

    with open('DataSeries.json','r') as data_series:
        Series_data = json.load(data_series)
        SIZE_OFF_SERIES_DATA = (len(Series_data['DataSeries']))

    for j in range(0,SIZE_OFF_SERIES_DATA):
        if int(Series_data['DataSeries'][j]['OrderTimestamp'])>int(last_time_dB):
            print(Series_data['DataSeries'][j])
            DeviceId = Series_data['DataSeries'][j]["DeviceId"]
            OrderTimestamp = Series_data['DataSeries'][j]['OrderTimestamp']
            DeviceValue = Series_data['DataSeries'][j]['DeviceValue']
            Alarm = Series_data['DataSeries'][j]['Alarm']
            put = table.put_item(
                Item={
                    'DeviceId':DeviceId,
                    'OrderTimestamp':OrderTimestamp,
                    'DeviceValue':DeviceValue,
                    'Alarm':Alarm
                }
            )
        #else:
        #    print("Nothing New")
