#*** PROGRAM : sendData_to_trama.py
#*** DESCRIPTION : Everything that happens and is not to scan DeviceConfigurations from DynamoDB !!
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+JA
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements: ( see in main_master.py comments, and in read_from_db.py comments)

import json
import time
from datetime import datetime
from zerofill import zerofill
from TradeAntenna import TradeAntenna
from data_process import data_process

def sendData_to_trama(DeviceId,DeviceSequence,Mac_slave):
    print("\n>>>>>>>>>>>>>>>>>>>sendData_to_trama!!!!\n")
    #time.sleep(5)
    trama = ""
    Mac_master = "24f7b5e350cc"  #MAC ADDRESS DO MASTER NECESSARIO ALTERAR SE O MASTER TIVER OUTRO MAC ADDRESS
    TramaType = "0"     #0equivalent to configuratio 1 - equivalent to broadcast

    MasterId = DeviceId[0][0:5]
    SlaveId = DeviceId[0][5:8]
    print("MasterId: ",MasterId)
    print("SlaveId: ",SlaveId)

#Lê valores de configurações dos DEVICE a partir do ficheir JSON para obter configuraçõs dos DEVICE
    with open('DeviceConfiguration.json','r') as data_device:
        Device_data = json.load(data_device)
        SIZE_OFF_DEVICE_DATA = (len(Device_data['DeviceConfiguration']))

#Idem para configurações dos SLAVE
    with open('SlaveConfiguration.json','r') as data_slave:
        Slave_data = json.load(data_slave)
        SIZE_OFF_SLAVE_DATA = len(Slave_data['SlaveConfiguration'])

#Obtém o ActuationParameter para o SLAVE em questão:
    ActuationParameter = []
    for x in range(0,SIZE_OFF_SLAVE_DATA):
        if SlaveId == Slave_data['SlaveConfiguration'][x]['SlaveId']and MasterId == Slave_data['SlaveConfiguration'][x]['MasterId']:
            ActuationParameter.append(Slave_data['SlaveConfiguration'][x]['ActuationParameter'])

    str_actuation = str(ActuationParameter[-1])

    SlopeConvertion = []
    InterceptConvertion = []
    DeviceType = []
    ReadType = []
    trama = ""
    for i in range(0,len(DeviceId)):
        #print("DeviceID: ",DeviceId[i])
        Slope = []
        Intercept = []
        Device_type = []
        Read_type = []
        #Carrega todas as configurações de DEVICES
        for x in range(0,SIZE_OFF_DEVICE_DATA):
            #Utiliza apenas as configurações mais recentes:
            if (DeviceId[i] == Device_data['DeviceConfiguration'][x]['DeviceId']):
                Slope.append(Device_data['DeviceConfiguration'][x]['SlopeConvertion'])
                Intercept.append(Device_data['DeviceConfiguration'][x]['InterceptConvertion'])
                Device_type.append(Device_data['DeviceConfiguration'][x]['DeviceType'])
                Read_type.append(Device_data['DeviceConfiguration'][x]['ReadType'])

        #Obter a ultima posição do array, ou seja os ados mais recentes
        if len(Slope) != 0:
            SlopeConvertion.append(Slope[-1])
        if len(Intercept) != 0:
            InterceptConvertion.append(Intercept[-1])
        if len(Device_type)!=0:
            DeviceType.append(Device_type[-1])
        if len(Read_type)!=0:
            ReadType.append(Read_type[-1])
    # print(SlopeConvertion)
    # print(InterceptConvertion)
    # print(DeviceType)
    # print(ReadType)

#Passa o valor do array para uma string, ou seja, aqui é que converte os paramtros na TRAMA:
    str_Slope =""
    str_Inter =""
    str_DeviceType = ""
    str_ReadType = ""
    for j in range(0,len(SlopeConvertion)):
        str_Slope = str_Slope + SlopeConvertion[j]
    for j in range(0,len(InterceptConvertion)):
        str_Inter = str_Inter + InterceptConvertion[j]
    for j in range(0,len(DeviceType)):
        str_DeviceType = str_DeviceType + DeviceType[j]
    str_DeviceType = str_DeviceType.replace(" ","")
    for j in range(0,len(ReadType)):
        str_ReadType = str_ReadType + ReadType[j]
    # print(str_DeviceType)

#Preenchimento com zeros para atingir o comprimento definido:
    if len(DeviceSequence)!=60:
        DeviceSequence = zerofill(DeviceSequence,60)
    if len(str_ReadType)!=15:
        str_ReadType = zerofill(str_ReadType,15)
    if len(str_DeviceType)!=45:
        str_DeviceType = zerofill(str_DeviceType,45)
    if len(str_Slope)!=150:
        str_Slope = zerofill(str_Slope,150)
    if len(str_Inter)!=150:
        str_Inter = zerofill(str_Inter,150)
    if len(str_actuation)!=20:
        str_rulle = zerofill(str_actuation,20)

    #trama de configuration
    print("rulle: ",str_rulle)
    trama =Mac_slave+TramaType+MasterId+SlaveId+DeviceSequence+str_ReadType+str_DeviceType+str_Slope+str_Inter+str_rulle
    print(len(trama), trama)

    nowd = datetime.now()
    nowd = nowd.strftime("%d/%m/%Y %H:%M:%S")
    print(">>>> READING SLAVES....",nowd)

#Envio da TAMA para o MASTER micrococontroller:
#Comunicação via série para o microcontrolador, e receção do que lá estiver para receber
    response = TradeAntenna(trama)      
    str_response = str(response)
    print(str_response)
    recv_trama = ""
    for x in range(0,len(response)):
        recv_trama = (response[x])
    print("recv_trama:", recv_trama)
    print(len(str_response))
    if len(recv_trama)==297:
        data_process(recv_trama)            #Processa toda a informação recebida do SLAVE, gera alarmes, faz broadcast e escreve informação no ficheiro DataSeries.json
    else:
        print("SLAVE NOT RESPONDING -> SIZE: ",len(recv_trama))

    print("\nwaiting for next slave<<<<<<<<<<<<<\n")
    #time.sleep(5)
    #time.sleep(5)
    # print(time.sleep(30))
