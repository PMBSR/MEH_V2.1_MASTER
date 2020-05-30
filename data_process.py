#*** PROGRAM : data_process.py
#*** DESCRIPTION : Process received data from MASTER MICROCONTROLLER, process alarms, send alarms, broadcast DeviceValues etc!!!
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+JA
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements: ( see in main_master.py comments, and in read_from_db.py comments)


# TRAMA DE RECEÇAO
# |Mac_Slave|Numberofreadings|----DeviceIDs-----|--------Values------|Ended
#               (2bits)       (12bits per device)    (6 bits per value)
#
import json
import time
from broadcasting import broadcasting
from datetime import datetime
from sendAlarm import sendAlarm
from decimal import Decimal
from im_connected import im_connected

def data_process(recv_trama):
    print("\nData process>>>>>>>>>>>>>>>>>>")
    #time.sleep(5)
    trama_size = len(recv_trama)

    # print("REcv: ",recv_trama)
    recv_trama = recv_trama[25:trama_size]
    print("\nAfter Recv",recv_trama)
    #print("size: ",len(recv_trama))

    Reading_Num = ""
    str_DeviceId = ""
    str_Values = ""
    #Percorrer a TRAMA, interpreta e coloca em estrutura de dados:
    for i in range(0,len(recv_trama)):
        if i<2:
            Reading_Num = Reading_Num+recv_trama[i]
        if i>=2 and i<=181:
            str_DeviceId = str_DeviceId+recv_trama[i]
        if i>181 and i<=trama_size:
            str_Values = str_Values+recv_trama[i]

    #print("Devices",str_DeviceId)
    print("readnum: ", Reading_Num)
    #print("Values ",str_Values)

    #Valores de leitura vêm com 6 digitos para cada valor, perfazendo 6X15=90 digitos
    #DeviceId vêm em 15 digitos por cada um portanto 12X15=180 digitos
    DeviceId_aux = []
    for x in range(0,len(str_DeviceId)):
        if (x)%12 == 0:
            DeviceId_aux.append(str_DeviceId[x:x+12])
    DeviceId = []
    #Se "x" for zeros é porque esta parte da TAMA não tem dados úteis ( por exemplo é uma parte correspondente a portas que não têm nenhum DEVICE
    #Ou seja, a TRAMA tem sempre a dimensão máxima que algumas vez pudesse ter! Isto pode ser otimizado
    for x in DeviceId_aux:
        if x!="000000000000":
            DeviceId.append(x)

    #Idem para valores
    Values_aux = []
    for j in range(0,len(str_Values)):
        if j%6==0:
            Values_aux.append(str_Values[j:j+6])

    #Idem para valores
    Values = []
    for x in range(0,len(Values_aux)):
        if x>=(len(Values_aux)-len(DeviceId)) and x<=len(Values_aux):
            Values.append(Values_aux[x])
    print("DeviceId:",DeviceId)
    print("Values:",Values)

    #Acontece que o SLAVE faz CEGAMENTE o preenchimento de zeros à esquerda qualquer que seja o valor
    #que encia para o MASTER. Mesmo que o valor seja negativo, por exmeplo "-2" é enviado como "0000000000-2"
    #A proxima parcela de codigo é para retirar esses zeros
    Values_final = []
    for x in Values:
        str_v = ""
        i = 0
        while x[i] == "0":
            i = i+1
        while i!=6:
            str_v = str_v + x[i]
            i=i+1
        Values_final.append(str_v)

    print("Values:--->", Values_final )


    #Aqui vai ler ao JSON os valores dos alarmes para validar e enviar alarmes:
    with open('DeviceConfiguration.json','r') as data_device:
        Device_data = json.load(data_device)
        SIZE_OFF_DEVICE_DATA = (len(Device_data['DeviceConfiguration']))

    #Idem para SLAVE
    with open('SlaveConfiguration.json','r') as data_slave:
        Slave_data = json.load(data_slave)
        SIZE_OFF_SLAVE_DATA = len(Slave_data['SlaveConfiguration'])

    #Vai fazer processamento de alarmes e também verificar quais da leiturtas recebidas estão em broadcast
    Alarm = ""
    DeviceBroadcast = []
    ArrayAlarms = []
    for d in range(0,len(DeviceId)):
        AlarmLowerLimit_all = []
        AlarmUpperLimit_all = []
        DeviceBroadcast_all = []
        Alarm_str = ""
        for de in range(0,SIZE_OFF_DEVICE_DATA):
            if DeviceId[d]==Device_data['DeviceConfiguration'][de]['DeviceId']:
                AlarmUpperLimit_all.append(Device_data['DeviceConfiguration'][de]['AlarmUpperLimit'])
                AlarmLowerLimit_all.append(Device_data['DeviceConfiguration'][de]['AlarmLowerLimit'])
                DeviceBroadcast_all.append(Device_data['DeviceConfiguration'][de]['DeviceBroadcast'])
        #print("New")
        AlarmUpperLimit = int(AlarmUpperLimit_all[-1])
        AlarmLowerLimit = int(AlarmLowerLimit_all[-1])
        DeviceBroadcast_all = (DeviceBroadcast_all[-1])
        DeviceBroadcast.append(DeviceBroadcast_all[-1])
        #print(AlarmUpperLimit,"\n",AlarmLowerLimit,"\n",DeviceBroadcast_all)
        if float(Values_final[d])>AlarmUpperLimit or float(Values_final[d])<AlarmLowerLimit:
            Alarm_str = "WARNING-> "+"\n"+" DeviceId:"+str(DeviceId[d])+"\n"+" Value:"+str(Values_final[d])+"\n"+" AlarmUpperLimit:"+str(AlarmUpperLimit)+"\n"+" AlarmLowerLimit:"+str(AlarmLowerLimit)+"\n"
            ArrayAlarms.append("YES")
        else:
            ArrayAlarms.append("NO")

        Alarm = Alarm + Alarm_str
    print("Alarmes em array:",ArrayAlarms)

    #Aqui faz o envio dos alarmes que identificou:
    if len(Alarm)!=0:
        send_to = DeviceId[0][5:8]
        MasterId = DeviceId[0][0:5]
        SlaveId = DeviceId[0][5:8]
        with open('SlaveConfiguration.json','r') as data_slave:
            Slave_data = json.load(data_slave)
            SIZE_OFF_SLAVE_DATA = len(Slave_data['SlaveConfiguration'])
        Phone = []
        for x in range(0,SIZE_OFF_SLAVE_DATA):
            if MasterId == Slave_data['SlaveConfiguration'][x]['MasterId'] and SlaveId==Slave_data['SlaveConfiguration'][x]['SlaveId']:
                Phone.append(Slave_data['SlaveConfiguration'][x]['AlarmPhone'])
        Phone = Phone[-1]
        print("Telefone:",Phone)
        print(Alarm)

        #Verifica se tem acesso à internet para, caso não tenha,
        #não correr a função seguinte pois de outro modo dá erro.
        #Deste modo, se não tiver acesso à internet o alarme não é enviado,
        #nem agora nem mais tarde - apenas no DataSeries conseguiremos ver se foi caso de alarme ou não
        connected3 = im_connected()
        if connected3==1:
            sendAlarm(str(Phone),Alarm)    ###########DESATIVA

    ####verificar se o device esta em DeviceBroadcast
    #zero ou um para saber se está em broadcast
    print(DeviceId)
    print(DeviceBroadcast)
    str_broad = ""
    for x in DeviceBroadcast:
        str_broad = str_broad+x
    print(">>>>>>>>",int(str_broad),"<<<<<<<<<<<<")

    #
    if int(str_broad)!= 0:
        broadcasting(DeviceId, DeviceBroadcast,Values)
        print("BROADCASTING<<<<<<<<<<<<<<")

    now = datetime.now()
    now = now.strftime("%Y%m%d%H%M%S%f")
    OrderTimestamp =now[0:17]

    # Registo de leituras recebidas no JSON DataSerires
    print("write to Mem")
    for t in range(0,len(DeviceId)):
        data = {
            "DeviceId":DeviceId[t],
            "OrderTimestamp":OrderTimestamp,
            "DeviceValue":Values_final[t],
            "Alarm": ArrayAlarms[t]
        }
        def write_json(Series_data, filename = 'DataSeries.json'):
            with open(filename,'w') as f:
                json.dump(Series_data,f, indent=4)
        with open('DataSeries.json','r') as data_device:
            Series_data = json.load(data_device)
            temp = Series_data['DataSeries']
            temp.append(data)
        write_json(Series_data)
    print("<<<<<<<<End of process")
