#!/usr/bin/env python
# Echo client program

import socket
import time
import math

# python record.py --samples 1 --frequency 5 --config new_record_config.xml 

#constants
PI = math.pi

#set up the connection
HOST = "10.42.0.118" # The UR IP address
PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#sending commands

#set up the functions for gripper
f = open ("Gripper.script", "rb")   #Robotiq Gripper
l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)

#moving
Q0 = [0,PI/-2,0,PI/-2,0,0]
Q1 = [-1.95, -1.66, 1.71, -1.62, -1.56, 1.19]
Q3 = [1.3, -0.16, 0.54, -1.94, -1.47, 0.16]

moveQ0 = "movej({0}, a=2.0, v=0.8)\n".format(Q0)
moveQ1 = "movej({0}, a=2.0, v=0.8)\n".format(Q1)
moveQ3 = "movej({0}, a=2.0, v=0.8)\n".format(Q3)

s.send(bytes(moveQ0,'utf-8'))
time.sleep(1)
s.send(bytes(moveQ3,'utf-8'))
time.sleep(1)

#gripper control
s.send(bytes("rq_activate_and_wait ()\n",'utf-8'))
s.send(bytes("rq_close_and_wait ()\n",'utf-8'))
#s.send(bytes("rq_is_object_detected ()\n",'utf-8'))
time.sleep(1)

s.send(bytes(moveQ1,'utf-8'))
time.sleep(1)

s.send(bytes("rq_open_and_wait ()\n",'utf-8'))

#NOTE: this end is needed as the Gripper file is declaring a whole func called Gripper and the functions is only accessable inside that functions
s.send(bytes("end\n",'utf-8'))
time.sleep(0.1)

data = s.recv(1108)
s.close()

print ("received", repr(data))



