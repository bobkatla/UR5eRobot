import numpy as np
import pandas as pd
import socket
import time
import struct
import math
import subprocess
import sys
import os

#set up the connection

HOST = "10.10.10.7"
# HOST = "127.0.0.1"

PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("connection done\n")

threshold = -0.001
# joints = [0.7, -0.8, 0.4, -1.9, -1.6, 1.23]
# moving = "movej({0}, a=2.0, v=0.8)\n".format(joints)
# s.send(bytes(moving,'utf-8'))

while(True):

    subprocess.check_output(["python", "record.py", "--host", str(HOST), "--samples", "1", "--frequency", "125", "--config", "testforce.xml"])
    a = pd.read_csv("./robot_data.csv")

    joint3_force = a.loc[0][3]

    if joint3_force > threshold:
        print("UP")
        joints = [0.7, -0.8, 0.4, -2.9, -1.6, 1.23]
        moving = "movej({0}, a=2.0, v=2.8)\n".format(joints)
        s.send(bytes(moving,'utf-8'))
        time.sleep(1.5)
    else:
        print("DOWN")
        joints = [0.7, -0.8, 0.4, -1.9, -1.6, 1.23]
        moving = "movej({0}, a=2.0, v=0.8)\n".format(joints)
        s.send(bytes(moving,'utf-8'))
        time.sleep(1.5)