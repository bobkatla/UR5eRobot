import numpy as np
import pandas as pd
import socket
import time
import struct
import math
import subprocess

#constants
PI = math.pi

LEARNING_RATE = 0.1
DISCOUNT = 0.95

MAX = [1,1,1] #max is 1m for all x, y, z
MIN = [-1,-1,-1]  #min is 1m for all x, y, z

TIMES_TRAIN = 100

NUMBER_ACTION = 6

REWARD_ARRIVE = 1
REWARD_NOT = 0
PELNATY = -1

GOAL = [-0.1, 0.4, 0.2]
ERROR_RATE = 0.1

DISCRETE_SIZE = [20,20,20] #how to discretize based on the the x, y, z

start_q_table = None

# create the table with the size based on x, y, z and the number of action
if start_q_table is None:
    q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_SIZE + [NUMBER_ACTION]))
else: 
    print("something is waiting for you")

# Exploration settings
epsilon = 1  # not a constant, going to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = TIMES_TRAIN//2 #this is to get the integer value after divition
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

# setup functions
def takeAction(action, joint_index, s, h):
    joints = getCurrentJoints(h).values.tolist()
    rad_pos = convertPosToRadPos(action)
    joints[joint_index] = rad_pos
    moving = "movej({0}, a=2.0, v=0.8)\n".format(joints)
    s.send(bytes(moving,'utf-8'))
    time.sleep(5)

def getDiscretePosX(x, i):
    # getting the size for each chunk after discretizing
    size_x = (MAX[i] - MIN[i])/DISCRETE_SIZE[i] 
    pos_x = x//size_x
    if pos_x < 0: 
        pos_x = DISCRETE_SIZE[i]//2 + pos_x
    return pos_x

# this will return the position in the table

def getStateDiscrete(xyz):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]

    pos_x = int(getDiscretePosX(x, 0))
    pos_y = int(getDiscretePosX(y, 1))
    pos_z = int(getDiscretePosX(z, 2))

    return pos_x, pos_y, pos_z    

def getCurrentXYZ(h):
    # getting the x, y, z position of the robot
    subprocess.check_output(["python", "record.py", "--host", str(h), "--samples", "1", "--frequency", "5", "--config", "xyz_record_config.xml"])
    # test1 = str(result_xyz)
    # print(test1)
    a = pd.read_csv("./robot_data.csv")
    actual_xyz = a.loc[0,:]
    result = actual_xyz[0:3]
    # print(result)
    # print(b)

    return result

def convertPosToRadPos(pos):
    a = NUMBER_ACTION // 2
    size = 2*PI/NUMBER_ACTION
    pos = pos - a
    return pos*size

def getCurrentJoints(h):
    # getting the current position of each joint of the robot
    subprocess.check_output(["python", "record.py", "--host", str(h), "--samples", "1", "--frequency", "5", "--config", "curQ_record_config.xml"])
    # test2 = str(result_joints)
    # print(test2)
    c = pd.read_csv("./robot_data.csv")
    actual_joints = c.loc[0,:]
    # print(d)

    return actual_joints

def distanceInXYZ(firstXYZ, secondXYZ):
    result = 0
    for i in range(3):
        a = firstXYZ[i] - secondXYZ[i]
        b = pow(abs(a), 2)
        result = result + b
    result = math.sqrt(result)
    return result

# def rewardFunc(current_XYZ):
#     distance = distanceInXYZ(current_XYZ, GOAL)*-1
#     return distance

#set up the connection

# HOST = "10.10.10.7"
HOST = "127.0.0.1"

PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("connection done\n")

for run_no in range(TIMES_TRAIN):
    discrete_state = getStateDiscrete(getCurrentXYZ(HOST))
    goal_discrete = getStateDiscrete(GOAL)
    done = False

    print("ok before while")

    while not done:
        if np.random.random() > epsilon:
            # get action from the Q-table
            action = np.argmax(q_table[discrete_state])
        else: 
            # Get random action
            action = np.random.randint(0, NUMBER_ACTION)
        
        #testing now with 1 joint
        takeAction(action, 0, s, HOST)

        new_XYZ = getCurrentXYZ(HOST)

        new_state_discrete = getStateDiscrete(new_XYZ)

        distance_goal = distanceInXYZ(new_XYZ, GOAL)

        reward = distance_goal * -1

        # Maximum possible Q value in next step (for new state)
        max_future_q = np.max(q_table[new_state_discrete])

        # Current Q value (for current state and performed action)
        current_q = q_table[discrete_state + (action,)]

        # And here's our equation for a new Q value for current state and action
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        # Update Q table with new Q value
        q_table[discrete_state + (action,)] = new_q

        if distance_goal < ERROR_RATE:
            done = True

        # Decaying is being done every episode if episode number is within decaying range
    if END_EPSILON_DECAYING >= run_no >= START_EPSILON_DECAYING:
        epsilon -= epsilon_decay_value

    print("the running is ok for the run no:", run_no)
    print("epsilon is:", epsilon)

np.save(f"./qtableUR5e.npy", q_table)
s.close()