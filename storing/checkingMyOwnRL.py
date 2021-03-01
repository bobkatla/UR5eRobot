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

print("connection done")

s.close()