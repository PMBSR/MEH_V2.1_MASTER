# Este Script faz verificação do disco de armazenamento, indicando o espaço livre e alertando
# o utilizador caso o espaço seja inferior a 200MB (pouco espaço)
# Faz verificação se a antena master se encontra corretamente ligada à RaspBerry
# JA+MC

import serial
import shutil               # para verificar disco
from time import sleep
from datetime import datetime

def init():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("WELCOME   ", now)
    print("CHECKING DISK ....")
    total, used, free = shutil.disk_usage("/")
    print("\n|Total Disk: %d GiB" % (total // (2**30)))
    print("|Used: %d GiB     " % (used // (2**30)))
    print("|Free: %d GiB     " % (free // (2**30)))
    if (used >= total - 0.800):
        print('\n -> WARNING! Only 200MB memory left!')
    else:
        print('\n -> DISK OKAY\n')

        #   checking antenna connection
        print('\nChecking Antenna Status ...')
        try:
            ser = serial.Serial('/dev/ttyUSB0', 115200) # if not works, -- try on terminal: python -m serial.tools.list_ports -- to see all ports found e substituir
            print("\nCHECK!")
        except serial.serialutil.SerialException:
            print (" \n----------  MASTER Antenna not connected! -------------\n ")
            print (" ERROR! Review ports ('/dev/ttyUSBX', 115200) !! [line 35 - init.py] ")
            print ("   || Try: '>>python -m serial.tools.list_ports' --> to see all ports found")
            # se o problema persistir, tentar no terminal: sudo chmod 777 /dev/ttyUSBx , onde x é a porta definida na linha 35
