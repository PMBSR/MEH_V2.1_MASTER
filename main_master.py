#*** PROGRAM : main_master.py
#*** DESCRIPTION : Main program to MASTER_RPI
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements:
#***
#****** URGENT!! : In some py files there is direct reference to THIS MASTER's MasterId by hardcode! This MUST be
#****** substituted urgently by a configuration file, or by the reading of the folder name, as the program is
#****** expected to be used by more than one MASTER.
#******
#****** This program should have 4 lines only:
#******** line 1: Scan DeviceConfigurations from DeviceConfigurations in DynamoDB, and dump them to JSON
#******** line 2: Send DeviceConfigurations, receive DeviceValues and send DeviceValues BROADCAST, to and
#********         from MASTER MICROCONTROLLER, and dump DeviceValues received to JSON
#******** line 3: Process and send Alarms
#******** line 4: Put DeviceValues to DataSeries in DataSeries, in DynamoDB
#******
#****** The files called by this program, and the ones called be those and so on, should all be reviewed,
#****** because actually:
#****** main_master.py
#******** read_from_db.py
#********** getData_from_DB.py
#******** search_json.py
#********** sendData_to_trama.py
#************ TradeAntenna.py
#************ data_process.py
#************** SendAlarm.py
#************** broadcasting.py
#**************** TradeAntenna.py
#******
#****** The JSON files for DeviceConfigurations should be only one file,
#****** and not one for Devices and another for Slaves
#******
#****** The JSON files should be used only as backup for in-memory data structures,
#****** and not as a database to be scanned to obtain data to run this program
#******  
#****** All the code should be as independent for the phisical meaning of the data as possible,
#****** reducing the need for code modifications when more parameters are added
#******
#****** For communication with MASTER MICROCONTROLLER the FRAME should have variable lenght
#****** depending on the lenght of the data that has real significance and use. Should not be
#****** filled with "0" (zeroes) to occupy the space of unsed ports of the SLAVE
#******
#****** DeviceConfigurations and DeviceValues should have a variable lenght
#****** depending on the lenght of the data with real significance, and not
#****** be filled with "0" (zeroes) to conform to a maximum size.

import json
import time
from search_json import search_json
from read_from_db import read_from_db
from update_dB import update_dB
from init import init
from im_connected import im_connected

flag = 1

init()

while(1):

    if flag==1:
        with open('DataSeries.json','r') as data_series:
            Series_data = json.load(data_series)
            SIZE_OFF_SERIES_DATA = (len(Series_data['DataSeries']))

#Vê qual o ultimo timestamp no ficheiro JSON DataŜerires
#Só vai ver se a FLAG for "1"
#FLAG é "1" no arranque e quando é feito o update à DataSeries
#Se não conseguir fazer o update da DataSeries então a FLAG fica a "0"
        for i in range(0,SIZE_OFF_SERIES_DATA):
            lastwrite = Series_data['DataSeries'][i]['OrderTimestamp']
    # print("flag: ", flag)
    # print("ola: ",lastwrite)
    connection1 = im_connected()
    if connection1 == 1:
        print(">>>>>>>> Consulting DynamodB...")
        read_from_db()
        print("<<<<<<<< I'm back from Dynamo")
    else:
        print("No connection detected for download")

#Esta função "search_json()" é a função dentro da qual TODA A PROGRAMAÇÃO QUE LIDA COM OS SLAVE ocorre !!!! 
    print("\n\nStart Readings\n\n")
    search_json()

    # print("MAIN <<<<<<<<<<<<<<<<")
    #print("10seg")
    #time.sleep(10)
    connection2 = im_connected()
    if connection2 == 1:
        flag = 1
        print("Updating DynamodB...")
        update_dB(lastwrite)
        print("Updated")
    else:
        flag = 0
        print("No connection detected for upload")

    time.sleep(60)
