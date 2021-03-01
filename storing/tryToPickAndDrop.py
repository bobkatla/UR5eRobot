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

#set up the functions for gripper
f = open ("Gripper.script", "rb")   #Robotiq Gripper
l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)

#moving
Q0 = [0,PI/-2,0,PI/-2,0,0]
Q1 = [-1.95, -1.66, 1.71, -1.62, -1.56, 1.19]
Q3 = [1.2, -0.16, 0.54, -1.94, -1.47, 0.16]
Q4 = [1.4, -0.16, 0.54, -1.94, -1.47, 0.16]

moveQ0 = "movej({0}, a=2.0, v=0.8)\n".format(Q0)
moveQ1 = "movej({0}, a=2.0, v=0.8)\n".format(Q1)
moveQ3 = " movej({0}, a=2.0, v=0.8)\n".format(Q3)
moveQ4 = " movej({0}, a=2.0, v=0.8)\n".format(Q4)

s.send(bytes(moveQ0,'utf-8'))
time.sleep(2)
s.send(bytes(moveQ3,'utf-8'))
time.sleep(1)
#gripper control
s.send(bytes("check = False\n",'utf-8'))
s.send(bytes("i = 0\n",'utf-8'))
s.send(bytes("mv = {0}\n".format(Q4),'utf-8'))
s.send(bytes("rq_activate_and_wait ()\n",'utf-8'))

tetsMove = " movej(mv, a=2.0, v=0.8)\n"

# s.send(bytes("rq_open_and_wait ()\n",'utf-8'))
# s.send(bytes("rq_close_and_wait ()\n",'utf-8'))
# s.send(bytes("check = rq_is_object_detected ()\n",'utf-8'))
# s.send(bytes("textmsg(check)\n",'utf-8'))
# s.send(bytes("if (not check):\n textmsg(\"no\")\n else:\n textmsg(\"yes\")\n end\n",'utf-8'))
# s.send(bytes("while(not check):\n rq_open_and_wait ()\n rq_close_and_wait ()\n check = rq_is_object_detected ()\n textmsg(check)\n end\n",'utf-8'))

startWhile = "while(not check):\n"
end = " end\n"
openGrip = " rq_open_and_wait ()\n"
closeRip = " rq_close_and_wait ()\n"
checkObject = " check = rq_is_object_detected ()\n"
startIf = " if (i%2 == 0):\n"
iPlus = " i = i + 1"
startElse = " else:\n"
changPos = " mv[0] = mv[0] + (i/100)\n"
changNeg = " mv[0] = mv[0] - (i/100)\n"

setChecking = openGrip + closeRip + checkObject
fullCom = startWhile + startIf + changPos + tetsMove + setChecking + startElse + changNeg + tetsMove + setChecking + end + iPlus + end
testWithout = startWhile + setChecking + end

s.send(bytes(fullCom,'utf-8'))

s.send(bytes(moveQ1,'utf-8'))
time.sleep(1)

# data = s.recv(1116)
# # get the digital output
# test = struct.unpack('!d', data[1044:1052])

s.send(bytes("rq_open_and_wait ()\n",'utf-8'))

#NOTE: this end is needed as the Gripper file is declaring a whole func called Gripper and the functions is only accessable inside that functions
s.send(bytes("end\n",'utf-8'))
time.sleep(0.1)
s.close()
# print (test)


