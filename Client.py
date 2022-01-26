#!/usr/bin/python3           # This is client.py file

import socket
import json

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = 'INSERT THE SERVER IP ADDRSSE' #To find IP addrsse of the server, go to cmd and type "ipconfig /all" on windows or "ifconfig" on Rasberry Pi

port = 9999
s.connect((host, port))
while True:
# connection to hostname on the port.

# Receive no more than 1024 bytes
    msg = s.recv(1024)

    print (msg.decode('UTF-8'))

