#*** PROGRAM : USER_InsertConfigurations.py
#*** DESCRIPTION : Insert data in DeviceConfigurations, in DynamoDB, for testing or first configuration
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+AF
#*** VERSION: 2.0 DATE: 20200526 AUTHOR: PSR MODIFICATIONS: Complete re-writing, better code organization and UX
#*** Possible improvement: better code organization, use functions to reuse code

import json
import time
import boto3

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from zerofill import zerofill
from datetime import datetime


SLAVE_ID_SIZE           = 3
MASTER_ID_SIZE          = 5
DEVICE_ID_SIZE          = 10
TANK_ID_SIZE            = 2
PORT_ID_SIZE            = 2
MULTIPLEX_ID_SIZE       = 2
SLOPE_SIZE              = 10
INTERCEPT_SIZE          = 10
MAC_ADDRESS_SIZE        = 12
ALARM_PHONE_SIZE        = 9
DEVICE_TYPE_OPTIONS     = ["PHH","ECC","LVL","TPS","TEM","TEM1","LUX"] 

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('DeviceConfigurations')

print("""InsertConfigurations.py:
(Inserts ON-LINE in DeviceConfigurations table)""")

#Print menu for the user:
reply=""
while reply!="1" and reply!="2" and reply!="3" and reply!="X" and reply!="x":
    print("""
    Press 1 to insert a new MASTER
    Press 2 to insert a new SLAVE
    Press 3 to insert a new DEVICE
    Press X to exit
    """)
    reply=input()
    
#insert a new MASTER:    
if reply=="1":
    print("Insert a new MASTER still not ready!\n")
    
#insert a new SLAVE:
elif reply=="2":
    print("\nInsert you data for a new SLAVE:")
    
    MasterId = input("MasterId: ")
    while str(MasterId)=="":
        MasterId = input("MasterId: ")
    MasterId = zerofill(MasterId,MASTER_ID_SIZE)

    SlaveId = input("SlaveId: ")
    while str(SlaveId)=="":
        SlaveId = input("SlaveId: ")
    SlaveId = zerofill(SlaveId,SLAVE_ID_SIZE)

    DeviceId = str(MasterId)+str(SlaveId)+"0000"
    print("DeviceId:",DeviceId,"\n")

    DeviceSequence = input("Device Sequence: (format: xxxx-xxxx)")
    if str(DeviceSequence)=="":
        DeviceSequence ="0"

    AlarmPhone = input("AlarmPhone: ")
    while(len(AlarmPhone)!=ALARM_PHONE_SIZE):
        print("ERROR AlarmPhone size expected is ",ALARM_PHONE_SIZE," digits\nNew try: ")
        AlarmPhone = input("AlarmPhone: ")

    ActuationParameter = input("ActuationParameter: ")
    if str(ActuationParameter)=="":
        ActuationParameter ="0"

    MacAddress = input("MacAddress: ")
    while(len(MacAddress)!=MAC_ADDRESS_SIZE):
        print("ERROR Wrong MacAddress size\nNew try: ")
        MacAddress = input("MacAddress: ")

    DeviceStatus = input("SlaveStatus: ")
    if str(DeviceStatus)=="":
        DeviceStatus ="0"

    now = datetime.now()
    now = now.strftime("%Y%m%d%H%M%S%f")
    now = now[0:17]
    
#Show data received from user:
    print("\nYou inserted:")
    print("\n")
    print("DeviceId          :  ",DeviceId)
    print("OrderTimestamp    :  ",now)
    print("\n")
    print("MasterId          :  ",MasterId)
    print("SlaveId           :  ",SlaveId)
    print("\n")
    print("DeviceStatus      :  ",DeviceStatus)
    print("DeviceSequence    :  ",DeviceSequence)
    print("AlarmPhone        :  ",AlarmPhone)
    print("MacAddress        :  ",MacAddress)
    print("ActuationParameter:  ",ActuationParameter)
    
#Ask user for confirmation, if "Y" insert it into ON-LINE DB:    
    print("\nConfirm? (Y/N) :   ")
    reply=input()
    if reply=="Y" or reply=="y":
        table.put_item(
            Item ={
                "DeviceId":DeviceId,
                "SlaveId":SlaveId,
                "OrderTimestamp":now,
                "MasterId":MasterId,
                "DeviceSequence":DeviceSequence,
                "AlarmPhone":AlarmPhone,
                "MacAddress":MacAddress,
                "DeviceStatus":DeviceStatus,
                "ActuationParameter":ActuationParameter
            })
        print("Your data was sent to ON-LINE DB")

#insert a new DEVICE:
elif reply=="3":
    print("\nInsert you data for a new DEVICE:")

#DeviceId receive from USER:
    DeviceId = input("DeviceId            :    ")
    while len(str(DeviceId))!=12:
        DeviceId = input("DeviceId            :   ")

#MasterId fill from DeviceId:
    MasterId = str(DeviceId[0:5])
    print("MasterId            :    ",MasterId)

#SlaveId fill from DeviceId:
    SlaveId = str(DeviceId[5:8])
    print("SlaveId             :    ",SlaveId)
    
#PortId fill from DeviceId:
    PortId = str(DeviceId[8:10])
    print("PortId              :    ",PortId)
    
#MultiplexId fill from DeviceId:
    MultiplexId = str(DeviceId[10:12])
    print("MultiplexId         :    ",MultiplexId)

#DeviceStatus receive from USER:
    DeviceStatus = input("DeviceStatus (0/1)  :    ")

#Fill unused attributes automatically:
    DeviceSequence = ""
    AlarmPhone = ""
    MacAddress = ""
    ActuationParameter = ""

#AmbientId receive from USER:
    AmbientId = input("AmbientId(0-Ex 1-In):    ")
    while str(AmbientId)!= "0" and str(AmbientId)!= "1":
        AmbientId = input("AmbientId (0/1)     :   ")

#TankId receive from USER:
    TankId = input("TankId (00 to 99)   :    ")
    if str(TankId)=="":
        TankId ="0"
    TankId = zerofill(TankId,TANK_ID_SIZE)

#DeviceType receive from USER:
    reply=""
    DeviceType = ""
    while DeviceType not in DEVICE_TYPE_OPTIONS:
        print("DeviceType options:", DEVICE_TYPE_OPTIONS)
        DeviceType = input("DeviceType          :    ")

#MeasureUnit receive from USER:
    MeasureUnit = input("MeasureUnit         :    ")
    if str(MeasureUnit)=="":
        MeasureUnit ="0"

#SlopeConvertion receive from USER:
    SlopeConvertion = input("SlopeConvertion     :    ")
    if str(SlopeConvertion)=="":
        SlopeConvertion = "1"

#InterceptConvertion receive from USER:
    InterceptConvertion = input("InterceptConvertion :    ")
    if str(InterceptConvertion)=="":
        InterceptConvertion = "0"

#AlarmUpperLimit receive from USER:
    AlarmUpperLimit = input("AlarmUpperLimit     :    ")
    while(AlarmUpperLimit == "" or AlarmUpperLimit.isalpha() == True):
        AlarmUpperLimit = input("Insert Again:")

#AlarmLowerLimit receive from USER:
    AlarmLowerLimit = input("AlarmLowerLimit     :    ")
    while(AlarmLowerLimit=="" or AlarmLowerLimit.isalpha() ==True):
        AlarmLowerLimit = input("Insert Again:")

#DevicePeriod receive from USER:
    DevicePeriod = input("DevicePeriod(minute):    ")
    if str(DevicePeriod)=="":
        DevicePeriod ="0"

#DeviceBroadCast receive from USER:
    DeviceBroadcast = input("DeviceBroadcast(0/1):    ")
    while str(DeviceBroadcast)=="":
        DeviceBroadcast = input("DeviceBroadcast(0/1):    ")

#MeasureName receive from USER:
    MeasureName = input("MeasureName         :    ")
    
#ReadType receive from USER:
    ReadType = input("ReadType(0/1)       :    ")
    while(ReadType==""):
        ReadType = input("ReadType(0/1)       :    ")

#OrderTimestamp fill from datetime:
    nowd = datetime.now()
    nowd = nowd.strftime("%Y%m%d%H%M%S%f")
    OrderTimestamp = nowd[0:17]
    
#Show data received from user for the new DEVICE:
    print("\nYou inserted:")
    print("\n")
    print("DeviceId            :  ",DeviceId)
    print("OrderTimestamp      :  ",OrderTimestamp)
    print("\n")
    print("MasterId            :  ",MasterId)
    print("SlaveId             :  ",SlaveId)
    print("PortId              :  ",PortId)
    print("MultiplexId         :  ",MultiplexId)
    print("\n")
    print("DeviceStatus        :  ",DeviceStatus)
    print("DeviceSequence      :  ",DeviceSequence)
    print("AlarmPhone          :  ",AlarmPhone)
    print("MacAddress          :  ",MacAddress)
    print("ActuationParameter  :  ",ActuationParameter)
    print("AlarmUpperLimit     :  ",AlarmUpperLimit)
    print("AlarmLowerLimit     :  ",AlarmLowerLimit)
    print("AmbientId           :  ",AmbientId)
    print("DeviceBroadcast     :  ",DeviceBroadcast)
    print("DevicePeriod        :  ",DevicePeriod)
    print("DeviceType          :  ",DeviceType)
    print("SlopeConvertion     :  ",SlopeConvertion)
    print("InterceptConvertion :  ",InterceptConvertion)
    print("MeasureUnit         :  ",MeasureUnit)
    print("MeasureName         :  ",MeasureName)
    print("ReadType            :  ",ReadType)
    print("TankId              :  ",TankId)
   
#Ask user for confirmation, if "Y" insert it into ON-LINE DB:    
    print("\nConfirm? (Y/N) :   ")
    reply=input()
    if reply=="Y" or reply=="y":
        table.put_item(
            Item = {
                "DeviceId":DeviceId,
                "OrderTimestamp":nowd,
                "AlarmUpperLimit":AlarmUpperLimit,
                "AlarmLowerLimit":AlarmLowerLimit,
                "AmbientId":AmbientId,
                "DeviceBroadcast":DeviceBroadcast,
                "DevicePeriod":DevicePeriod,
                "DeviceType":DeviceType,
                "SlopeConvertion":SlopeConvertion,
                "InterceptConvertion":InterceptConvertion,
                "MeasureUnit":MeasureUnit,
                "MeasureName":MeasureName,
                "ReadType":ReadType,
                "TankId":TankId
            })
        print("Your data was sent to AWS DynamoDB DeviceConfigurations")
  
#Exit:
elif reply=="X" or reply=="x":
    print("Goodby!\n")
    
else:
    print("Error, reply not expected:",reply,"\n")
    
print("Thank you! Press any key to leave this program")

input()

