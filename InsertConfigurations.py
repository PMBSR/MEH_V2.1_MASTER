import json
import time
import boto3

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from zerofill import zerofill
from datetime import datetime


SLAVE_ID_SIZE 			= 3
MASTER_ID_SIZE			= 5
DEVICE_ID_SIZE			= 10
TANK_ID_SIZE			= 2
PORT_ID_SIZE			= 2
MULTIPLEX_ID_SIZE		= 2
SLOPE_SIZE				= 10
INTERCEPT_SIZE			= 10

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('DeviceConfigurations')

print("Do you want to insert a new Slave Configuration? (Y/N)\n")
if(input()=='y'):
	print("New Slave Configuration:\n")
	MasterId = input("MasterId: ")
	while str(MasterId)=="":
		MasterId = input("MasterId: ")
	MasterId = zerofill(MasterId,MASTER_ID_SIZE)

	SlaveId = input("SlaveId: ")
	while str(SlaveId)=="":
		SlaveId = input("SlaveId: ")
	SlaveId = zerofill(SlaveId,SLAVE_ID_SIZE)

	DeviceId = str(MasterId)+str(SlaveId)+"0000"

	DeviceSequence = input("Device Sequence: (format: xxxx-xxxx)")
	if str(DeviceSequence)=="":
		DeviceSequence ="0"

	AlarmPhone = input("AlarmPhone: ")
	while(len(AlarmPhone)!=9):
		print("ERROR Wrong AlarmPhone size\nNew try: ")
		AlarmPhone = input("AlarmPhone: ")

	ActuationParameter = input("Actuation parameter: ")
	if str(ActuationParameter)=="":
		ActuationParameter ="0"

	MacAddress = input("MacAddress: ")
	while(len(MacAddress)!=12):
		print("ERROR Wrong MacAddress size\nNew try: ")
		MacAddress = input("MacAddress: ")

	DeviceStatus = input("SlaveStatus: ")
	if str(DeviceStatus)=="":
		DeviceStatus ="0"

	now = datetime.now()
	now = now.strftime("%Y%m%d%H%M%S%f")
	now = now[0:17]
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
		}
	)

else:
	print("    -->      Next Step")

print("Do you want to insert a new Device Configuration? (Y/N)")
if(input()=='y'):
	print("New data for Device Configuration\n")

	DeviceId = input("Device ID: ")
	while len(str(DeviceId))!=12:
		DeviceId = input("Device ID:")

	AmbientId = input("Ambient ID(0/1): ")
	while str(AmbientId)=="":
		AmbientId = input("Ambient ID(0/1): ")

	TankId = input("Tank ID: ")
	if str(TankId)=="":
		TankId ="0"
	TankId = zerofill(TankId,TANK_ID_SIZE)

	DeviceType = input("DeviceType: ")
	while len(str(DeviceType))!=3:
		DeviceType = input("DeviceType: ")

	MeasureUnit = input("MeasureUnit: ")
	if str(MeasureUnit)=="":
		MeasureUnit ="0"

	SlopeConvertion = input("SlopeConvertion: ")
	if str(SlopeConvertion)=="":
		SlopeConvertion = "1"

	InterceptConvertion = input("InterceptConvertion: ")
	if str(InterceptConvertion)=="":
		InterceptConvertion = "0"

	AlarmUpperLimit = input("Alarm Upper Limit: ")
	while(AlarmUpperLimit == "" or AlarmUpperLimit.isalpha() == True):
		AlarmUpperLimit = input("Insert Again:")

	AlarmLowerLimit = input("Alarm Lower Limit: ")
	while(AlarmLowerLimit=="" or AlarmLowerLimit.isalpha() ==True):
		AlarmLowerLimit = input("Insert Again:")

	DevicePeriod = input("Device Period: ")
	if str(DevicePeriod)=="":
		DevicePeriod ="0"

	DeviceBroadcast = input("DeviceBroadcast(0/1): ")
	while str(DeviceBroadcast)=="":
		DeviceBroadcast = input("DeviceBroadcast(0/1): ")

	MeasureName = input("MeasureName: ")
	ReadType = input("ReadType(0/1): ")
	while(ReadType==""):
		ReadType = input("ReadType(0/1): ")

	nowd = datetime.now()
	nowd = nowd.strftime("%Y%m%d%H%M%S%f")
	nowd = nowd[0:17]

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
else:
	print("No new Device configured.")
	print("    -->      Exiting ....")
