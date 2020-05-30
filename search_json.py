#*** PROGRAM : search_json.py
#*** DESCRIPTION : Everything that happens and is not to scan DeviceConfigurations from DynamoDB !!
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+JA
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements: ( see in main_master.py comments, and in read_from_db.py comments)

import json
import time
from sendData_to_trama import sendData_to_trama
import threading

def search_json():
    print(">>>>>>>>SEARCH\n")

    MASTER_ID_ = "00001"    #SET MASTER ID####################################ex"00002" for master2

    print("\nMasterId: ",MASTER_ID_)

#Fazer load da informação que está no ficheiro JSON DeviceConfiguration
    with open('DeviceConfiguration.json','r') as data_device:
        Device_data = json.load(data_device)
        SIZE_OFF_DEVICE_DATA = (len(Device_data['DeviceConfiguration']))

#Fazer load da informação que está no ficheiro JSON SlaveConfiguration
#NOTA: MIGUEL PARTIU A INFORMAÇÃ DOS DEVICE CONFIGURATION EM DOIS FICHEIROS JSON UM PARA DEVICE OUTRO PARA SLAVE
    with open('SlaveConfiguration.json','r') as data_slave:
        Slave_data = json.load(data_slave)
        SIZE_OFF_SLAVE_DATA = len(Slave_data['SlaveConfiguration'])

#Permite saber quais os MASTERS que estão no ficheiro
#CODIGO INUTIL:
#    IdMaster = []
#    for i in range(0,SIZE_OFF_SLAVE_DATA):
#        IdMaster.append(Slave_data['SlaveConfiguration'][i]['MasterId'])
#    print("Total Masters in json: ", IdMaster)

#Retorna os SLAVES todos os SLAVES que estão agregados ao MASTER sem repetir nenhum:
    IdSlaves = []
    for x in range(0,SIZE_OFF_SLAVE_DATA):
        if MASTER_ID_ == Slave_data['SlaveConfiguration'][x]['MasterId']:
            IdSlaves.append(Slave_data['SlaveConfiguration'][x]['SlaveId'])
    print("Total Slaves in json: ",IdSlaves)
    Id_Slaves = []
    for x in IdSlaves:
        if x not in Id_Slaves:
            Id_Slaves.append(x)
    print("Total Slaves to Read: ",Id_Slaves)

#Depois de saber quais sã os seus SLAVE vai ao ficheiro JSON obter a informação mais recente de cada SLAVE
    for j in range(0,len(Id_Slaves)):
        Device_Sequence = []
        MasterId = []
        SlaveId = []
        Mac_slave = []
        DeviceStatus = []
        for k in range(0,SIZE_OFF_SLAVE_DATA):
            if(Id_Slaves[j] == Slave_data['SlaveConfiguration'][k]['SlaveId']and Slave_data['SlaveConfiguration'][k]['MasterId']==MASTER_ID_):
                Device_Sequence.append(Slave_data['SlaveConfiguration'][k]['DeviceSequence'])
                MasterId.append(Slave_data['SlaveConfiguration'][k]['MasterId'])
                SlaveId.append(Slave_data['SlaveConfiguration'][k]['SlaveId'])
                Mac_slave.append(Slave_data['SlaveConfiguration'][k]['MacAddress'])
                DeviceStatus.append(Slave_data['SlaveConfiguration'][k]['DeviceStatus'])
        MasterId = MasterId[-1]
        SlaveId = SlaveId[-1]
        Mac_slave = Mac_slave[-1]
        DeviceStatus = DeviceStatus[-1]
        print("Master: ",MasterId )
        print("Slave :" ,SlaveId)
        print("Mac_slave: ",Mac_slave)
        print("DeviceStatus: ",DeviceStatus)
        DeviceSequence = Device_Sequence[-1]
        DeviceSequence = DeviceSequence.replace('-','')
        print("DeviceSequence: ",DeviceSequence)

#Para SLAVE's ativos, contgroi a TAMA de configurações para lha enviar (a de cada SLAVE a cada SLAVE
        if DeviceStatus != "0":
            buffer = ""
            DeviceId = []
            for x in range(0,len(DeviceSequence)):
                buffer = buffer+DeviceSequence[x]
                if (x+1)%4==0:
                    str = MasterId + SlaveId + buffer    #DeviceId
                    DeviceId.append(str)
                    buffer =""
            print("\nDeviceId: ",DeviceId)
            #Aqui é que envia os parametros de configuração para a TRAMA que há-se seguir para o SLAVE
            sendData_to_trama(DeviceId,DeviceSequence,Mac_slave)
        else:
            print("\n <->SLAVE DOWN!!!!!<->\n")
