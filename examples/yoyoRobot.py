import numpy as np
import pandas as pd
import socket
import time
import struct
import math
import subprocess
import sys
import os
import asyncio

#set up the connection

HOST = "10.10.10.7"
# HOST = "127.0.0.1"

PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("connection done\n")

threshold = 0.1
# joints = [0.7, -0.8, 0.4, -1.9, -1.6, 1.23]
# moving = "movej({0}, a=2.0, v=0.8)\n".format(joints)
# s.send(bytes(moving,'utf-8'))

def getPoses(h):
    subprocess.check_output(["python", "record.py", "--host", str(h), "--samples", "1", "--frequency", "5", "--config", "curQ_record_config.xml"])
    a = pd.read_csv("./robot_data.csv")
    actual_q = a.loc[0,:]
    return actual_q

def comparePose(pose1, pose2):
    thres = 0.01
    for i in range(0,6):
        if pose1[i] < pose2[i] - thres or pose1[i] > pose2[i] + thres:
            return False
    return True

def moveTo(joints, a, v):
    moving = "movej({0}, a={1}, v={2})\n".format(joints, a, v)
    s.send(bytes(moving,'utf-8'))

while(True):

    subprocess.check_output(["python", "record.py", "--host", str(HOST), "--samples", "1", "--frequency", "125", "--config", "testforce.xml"])
    a = pd.read_csv("./robot_data.csv")

    joint3_force = a.loc[0][3]

    jointsUp = [0.7, -0.8, 0.4, -2.9, -1.6, 1.23]
    jointsDown =  [0.7, -0.8, 0.4, -1.9, -1.6, 1.23]
    currentPose = getPoses(HOST)

    # print(comparePose(currentPose, jointsDown))
    if joint3_force > threshold:
        if comparePose(currentPose, jointsDown):
            print("UP")
            moveTo(jointsUp, 2.0, 1.8)
            # # sleep
            # time.sleep(0.5)
    else:
        if comparePose(currentPose, jointsUp):
            print("DOWN")
            moveTo(jointsDown, 2.0, 0.8)
            # # sleep
            # time.sleep(0.5)