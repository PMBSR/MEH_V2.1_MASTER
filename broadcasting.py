#*** PROGRAM : broadcasting.py
#*** DESCRIPTION : Broadcast DeviceValues etc!!!
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+JA
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements: ( see in main_master.py comments, and in read_from_db.py comments)




import json
import time
from zerofill import zerofill
from TradeAntenna import TradeAntenna
from zerofill import zerofill

def broadcasting(DeviceId,DeviceBroadcast,Values):
    TramaType = "1"         ##envio de um trama de broadcast
    print("\n>>>>>>>BroadCasting\n")
    #time.sleep(5)
    # print("Devices",DeviceId)
    # print("Values",Values)
    # print(DeviceBroadcast)

    Slave_source = DeviceId[0]
    Slave_source = Slave_source[5:8]

    print("Slave Source",Slave_source)

    with open('DeviceConfiguration.json','r') as data_device:
        Device_data = json.load(data_device)
        SIZE_OFF_DEVICE_DATA = (len(Device_data['DeviceConfiguration']))

    with open('SlaveConfiguration.json','r') as data_slave:
        Slave_data = json.load(data_slave)
        SIZE_OFF_SLAVE_DATA = len(Slave_data['SlaveConfiguration'])


    BroadValues = []
    BroadDevice = []

    for x in range(0, len(DeviceBroadcast)):
       if DeviceBroadcast[x]=="1":
           BroadDevice.append(DeviceId[x])
           BroadValues.append(Values[x])

    print(BroadDevice)
    print(BroadValues)
    MasterId = BroadDevice[0][0:5]
    print("MASTER>>>:", MasterId)
    Totalbroadcasting = str(len(BroadDevice))
    Totalbroadcasting = zerofill(Totalbroadcasting,2)
    print("total: ", Totalbroadcasting)

    str_BroadDevice = ""
    for x in range(0,len(BroadDevice)):
        str_BroadDevice = str_BroadDevice+str(BroadDevice[x])
    #print("str:_", str_BroadDevice)
    if len(str_BroadDevice)!=180:
        str_BroadDevice = zerofill(str_BroadDevice,180)
    #print("str_",str_BroadDevice)

    str_BroadValues = ""
    for x in range(0,len(BroadValues)):
        str_BroadValues = str_BroadValues+str(BroadValues[x])
    #print("str:_", str_BroadValues)
    if len(str_BroadValues)!=90:
        str_BroadValues = zerofill(str_BroadValues,90)
    #print("str_",str_BroadValues)

    SlaveId = []
    Mac_Slave = []
    for i in range(0,SIZE_OFF_SLAVE_DATA):
        if Slave_source != Slave_data['SlaveConfiguration'][i]['SlaveId'] and MasterId == Slave_data['SlaveConfiguration'][i]['MasterId'] and Slave_data['SlaveConfiguration'][i]['DeviceStatus']=='1':
            SlaveId.append(Slave_data['SlaveConfiguration'][i]['SlaveId'])
    print("SLAVES ON: ", SlaveId)
    Id_Slave = []
    for x in SlaveId:
        if x not in Id_Slave:
            Id_Slave.append(x)
    #print("Destination: ", SlaveId)
    print("destination: ",Id_Slave)

    if int(Totalbroadcasting) != "0":
        for j in range(0, len(Id_Slave)):
            Mac_destination = []
            for k in range(0,SIZE_OFF_SLAVE_DATA):
                if Id_Slave[j] == Slave_data['SlaveConfiguration'][k]['SlaveId']and Slave_data['SlaveConfiguration'][k]['MasterId']==MasterId:
                    Mac_destination.append(Slave_data['SlaveConfiguration'][k]['MacAddress'])


            print(Mac_destination[-1])

            trama = Mac_destination[-1]+TramaType+Totalbroadcasting+str_BroadDevice+str_BroadValues

            #print("rec: ",TradeAntenna(trama))
            TradeAntenna(trama)
            print("trama send to:",Id_Slave[j],"\n",trama)
            print("Size: ",len(trama))
    else:
        print("No Broadcast Device founded")
    #time.sleep(3)
