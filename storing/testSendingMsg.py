#!/usr/bin/env python
# Echo client program

import numpy as np
import socket
import time
import struct
import math

#constants
PI = math.pi

#set up the connection
HOST = "10.10.10.7" # The UR IP address
PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#sending commands


s.send(bytes("powerdown()\n",'utf-8'))
time.sleep(1)
data = s.recv(1116)

# # get the digital output
# test = struct.unpack('!d', data[1044:1052])

s.close()

# print(test)

