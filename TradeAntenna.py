#*** PROGRAM : TradeAntenna.py
#*** DESCRIPTION : Receive data from MASTER MICROCONTROLLER and save it in JSON file in correct format
#*** VERSION: 1.0 DATE: 20200525 AUTHOR: MC+JA
#*** VERSION: 2.0 DATE: 202005302230 AUTHOR: PSR MODIFICATIONS: This header, some comments
#***
#*** Possible improvements: ( see in main_master.py comments, and in read_from_db.py comments)

import serial
import io
import json
import time
from datetime import datetime   # get actual date
# from data_process import data_process
# User guide:
# python -m serial.tools.list_ports -- to see all ports found
# turn serial connection on, if last command lists ttyUSB0 : sudo chmod 777 /dev/ttyUSB0

def TradeAntenna(trama):
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    print("\n>>>>>>>>>>>>>>>>>>Trade")
    recv = ""
    if ser.isOpen():
        ser.write(trama.encode())   # New trama is sended to LoRa Antenna in order to spread along the system
        print("...Sending info")
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S") # info Received timestamp

        rl1 = ser.readline().splitlines()
        recv =[rl1.decode('utf-8') for rl1 in rl1]
        #print("Recv:",recv)
    print("Trade<<<<<<<<<<<<<<<<<\n")
    return recv
        
