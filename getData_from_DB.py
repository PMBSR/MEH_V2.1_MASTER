#*** PROGRAM : read_from_db.py
#*** DESCRIPTION : Get all DeviceConfigurations from DynamoDB and write them to JSON
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+JA
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements: ( see in main_master.py comments, and in read_from_db.py comments)


from __future__ import print_function
import boto3
import json
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime

def getData_from_DB(last_OrderTimestamp):

    class DecimalEncoder(json.JSONEncoder):
        def default(self,o):
            if isinstance(o,decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    now = datetime.now()
    now = now.strftime("%Y%m%d%H%M%S%f")
    now =now[0:17]

    print("now: ",now)

    dynamodb = boto3.resource('dynamodb',region_name='us-east-2')
    table = dynamodb.Table('DeviceConfigurations')

#AQUI NA PROXIMA LINHA 'E ONDE É DEFINIDO QUAL O MASTER QUE ESTÁ A CORRER PARA FILTRAR OS DADOS RECOLHIDOS DA DeviceConfigurations
#Necessário ALTERAR SE MUDAR DE MASTER e necessario migrar esta configuração para um ficheiro externo qualquer
#O MASTER está indicado em HARDCODE NOUTROS PROGRAMAS, por EXEMPLO na search_json.py
    fe = Key('OrderTimestamp').between(str(last_OrderTimestamp),str(now)) & Key('DeviceId').begins_with("00001")
    pe = "#Device, OrderTimestamp, AlarmPhone, AlarmLowerLimit, AlarmUpperLimit, DeviceBroadcast,DevicePeriod, DeviceType, InterceptConvertion,SlopeConvertion, AmbientId, DeviceSequence, MacAddress, TankId, ReadType, DeviceStatus, ActuationParameter"
    ean = {"#Device":"DeviceId",}
    esk = None

    response = table.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
        )

    #for i in response['Items']:
    #    print(json.dumps(i, cls=DecimalEncoder))

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=fe,
            ProjectionExpression=pe,
            ExpressionAttributeNames=ean,
            ExclusiveStartKey=response['LastEvaluatedKey']
            )
    return response
