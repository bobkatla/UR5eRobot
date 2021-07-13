#!/usr/bin/env python
# Echo client program

import numpy as np
import socket
import time
import struct
import math
import subprocess

#constants
PI = math.pi

def getPoses(h):
    subprocess.check_output(["python", "record.py", "--host", str(h), "--samples", "1", "--frequency", "5", "--config", "curQ_record_config.xml"])
    a = pd.read_csv("./robot_data.csv")
    actual_q = a.loc[0,:]
    return actual_q

def comparePose(pose1, pose2):
    thres = 0.08
    for i in range(0,6):
        if pose1[i] < pose2[i] - thres or pose1[i] > pose2[i] + thres:
            return False
    return True

def moveTo(joints, a, v):
    moving = "movej({0}, a={1}, v={2})\n".format(joints, a, v)
    s.send(bytes(moving,'utf-8'))

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

Q3 = [1.2, -0.16, 0.54, -1.94, -1.47, 0.16]


moveQ0 = "movej({0}, a=2.0, v=0.8)\n".format(Q0)
moveQ3 = " movej({0}, a=2.0, v=0.8)\n".format(Q3)

# the pose to pick
Q4 = [1.15, -1.1, 1.95, -2.41, -1.58, 1.52]
moveQ4 = " movej({0}, a=2.0, v=0.8)\n".format(Q4)
# the pose to shake
Q1 = [2.35, -1.12, 1.32, -2.89, -1.19, -0.24]
moveQ1 = "movej({0}, a=2.0, v=0.8)\n".format(Q1)


s.send(bytes(moveQ0,'utf-8'))
time.sleep(2)
# s.send(bytes(moveQ3,'utf-8'))
time.sleep(1)
#gripper control
s.send(bytes("check = False\n",'utf-8'))
s.send(bytes("i = 0\n",'utf-8'))
s.send(bytes("mv = {0}\n".format(Q4),'utf-8'))
s.send(bytes("rq_activate_and_wait ()\n",'utf-8'))

tetsMove = " movej(mv, a=2.0, v=0.8)\n"


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

s.send(bytes("rq_open_and_wait ()\n",'utf-8'))

#NOTE: this end is needed as the Gripper file is declaring a whole func called Gripper and the functions is only accessable inside that functions
s.send(bytes("end\n",'utf-8'))
time.sleep(0.1)

nowP = getPoses(HOST)
while not comparePose(nowP, Q1):
    nowP = getPoses(HOST)

subprocess.check_output(["python", "record.py", "--host", str(HOST), "--samples", "1", "--frequency", "125", "--config", "testforce.xml"])
a = pd.read_csv("./robot_data.csv")
joint3_force = a.loc[0][3]

threshold = 0.01
while joint3_force < threshold:
    subprocess.check_output(["python", "record.py", "--host", str(HOST), "--samples", "1", "--frequency", "125", "--config", "testforce.xml"])
    a = pd.read_csv("./robot_data.csv")
    joint3_force = a.loc[0][3]
print("Yesss")
s.close()