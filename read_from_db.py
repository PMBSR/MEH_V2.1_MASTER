#*** PROGRAM : read_from_db.py
#*** DESCRIPTION : Get all DeviceConfigurations from DynamoDB and write them to JSON
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+JA
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements:
#***
#****** DeviceConfigurations are scanned from one table only (DeviceConfigurations) from DynamoDB
#****** Any DeviceId that has all the ritghside four digits equally to "0" is a SLAVE, and removing
#****** those four rightside "0" we have a SlaveId
#****** This program is splitting data scanned in DeviceConfigurations in DynamoDB in
#****** two JSON files, and working with these two files. This could be simplified if only one
#****** JSON file was used to all DeviceConfigurations as done in DynamoDB.
#******
#****** All this program should know is that there is a list of DeviceConfigurations to scan in
#****** DeviceConfigurations in DynamoDB and that shall send them to MASTER MICROCONTROLLER
#****** and ignore all other details.

import json
import time
from datetime import datetime
from zerofill import zerofill
from getData_from_DB import getData_from_DB

def read_from_db():
    #definnig some Macros
    SLAVE_ID_SIZE           = 3
    MASTER_ID_SIZE          = 5
    DEVICE_SEQUENCE_SIZE    = 60
    DEVICE_ID_SIZE          = 12
    TANK_ID_SIZE            = 2
    PORT_ID_SIZE            = 2
    MULTIPLEX_ID_SIZE       = 2
    SLOPE_SIZE              = 10
    INTERCEPT_SIZE          = 10


#Vai buscar o ultimo TIMESTAMP gravado no
    with open('DeviceConfiguration.json','r') as data_device:
        Device_data = json.load(data_device)
        SIZE_OFF_DEVICE_DATA =  (len(Device_data['DeviceConfiguration']))
    Device_last_time =Device_data['DeviceConfiguration'][-1]["OrderTimestamp"]

    with open('SlaveConfiguration.json','r') as data_slave:
        Slave_data = json.load(data_slave)
        SIZE_OFF_SLAVE_DATA =   (len(Slave_data['SlaveConfiguration']))
    Slave_last_time = Slave_data['SlaveConfiguration'][-1]['OrderTimestamp']

    print("\n","time 1: ", Device_last_time,"\n","time 2: ",Slave_last_time)

    #lets get all new configurations from dynamodB that are more recents
    if int(Device_last_time)<int(Slave_last_time):
        print("Using slave ", Slave_last_time)
        Slave_last_time = int(Slave_last_time)+1
        data = getData_from_DB(int(Slave_last_time))###consulta a base de dados online
    else:
        print("using Device: ")
        data = getData_from_DB(int(Device_last_time))
    #print("Recebido: ",data)
    # print(data['Items'][0])
    # print(data['Items'][1])
    # print(data['Items'][2])

    # print(len(data['Items']))

    #saving new Configurations to LOCAL DATA BASE
    for x in range(0,len(data['Items'])):
        DeviceId = data['Items'][x]["DeviceId"]
        if DeviceId[8:12] == "0000":
            SlaveId = DeviceId[5:8]
            MasterId = DeviceId[0:5]
            DeviceSequence = data['Items'][x]['DeviceSequence']
            ActuationParameter = data['Items'][x]['ActuationParameter']
            AlarmPhone = data['Items'][x]['AlarmPhone']
            OrderTimestamp =data['Items'][x]['OrderTimestamp']
            MacAddress = data['Items'][x]['MacAddress']
            DeviceStatus = data['Items'][x]["DeviceStatus"]
            s={
                "SlaveId":SlaveId,
                "OrderTimestamp":OrderTimestamp,
                "MasterId":MasterId,
                "DeviceSequence":DeviceSequence,
                "ActuationParameter":ActuationParameter,
                "AlarmPhone":AlarmPhone,
                "MacAddress":MacAddress,
                "DeviceStatus":DeviceStatus

                }
            # the next thing to do is to write the data into our json file, for later consultation
            def write_json(Slave_data, filename='SlaveConfiguration.json'):
                with open(filename,'w') as f:
                    json.dump(Slave_data, f, indent=4)
            with open('SlaveConfiguration.json') as json_file:
                Slave_data = json.load(json_file)
                temp = Slave_data['SlaveConfiguration']
                temp.append(s)
            write_json(Slave_data)
            print("Slave write")

        if DeviceId[8:12]!="0000":
            d0 = data['Items'][x]['DeviceId']
            d1 = data['Items'][x]['AmbientId']
            d2 = data['Items'][x]["TankId"]
            d2 = zerofill(d2,TANK_ID_SIZE)

            d5 = data['Items'][x]['DeviceType']
            d6 = str(data['Items'][x]["SlopeConvertion"])
            d6 = zerofill(d6,SLOPE_SIZE)
            d7 = str(data['Items'][x]["InterceptConvertion"])
            d7 = zerofill(d7,INTERCEPT_SIZE)
            d8 = str(data['Items'][x]["AlarmUpperLimit"])
            d9 = str(data['Items'][x]["AlarmLowerLimit"])
            d10 = str(data['Items'][x]["DevicePeriod"])
            d11 = str(data['Items'][x]["DeviceBroadcast"])
            #d12 = data['Items'][-1]["MacAddress"]
            OrderTimestamp = int(data['Items'][x]['OrderTimestamp'])+1
            OrderTimestamp =str(OrderTimestamp)
            ReadType = str(data['Items'][x]['ReadType'])
            d = {
                "DeviceId":d0,
                "OrderTimestamp":OrderTimestamp,
                "AmbientId":d1,
                "TankId":d2,
                "DeviceType":d5,
                "ReadType": ReadType,
                "SlopeConvertion":d6,
                "InterceptConvertion":d7,
                "AlarmUpperLimit":d8,
                "AlarmLowerLimit":d9,
                "DevicePeriod":d10,
                "DeviceBroadcast":d11
                }
            def write_json(Device_data, filename='DeviceConfiguration.json'):
                with open(filename,'w') as fd:
                    json.dump(Device_data, fd, indent=4)
            with open('DeviceConfiguration.json') as json_filed:
                Device_data = json.load(json_filed)
                tempd = Device_data['DeviceConfiguration']
                tempd.append(d)
            write_json(Device_data)
            print("Device write")
