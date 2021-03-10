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

EPISODES = 1009

NUMBER_ACTION = 6

# REWARD_ARRIVE = 1
# REWARD_NOT = 0
# PELNATY = -1

THE_TESTED_JOINTS = [0]
NUMBER_OF_JOINTS = len(THE_TESTED_JOINTS)

GOAL = [0.47, 0.34, 0.55] #the xyz goal of the robot
ERROR_RATE = 0.1

DISCRETE_SIZE = [20,20,20] #how to discretize based on the the x, y, z

start_q_table = None

# create the table with the size based on x, y, z and the number of action
if start_q_table is None:
    q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_SIZE + NUMBER_OF_JOINTS*[NUMBER_ACTION]))
else: 
    q_table = np.load(f"./qtableUR5e.npy")

# a = (1, 2, 3)
# a = a + (2, )
# print(a)
# for x in a:
#     print(x+1)
# print(np.size(q_table[a]))

# Exploration settings
epsilon = 0.9  # not a constant, going to be decayed
epsilon_decay_value = 1/EPISODES

# setup functions
def takeAction(action, s, h):
    joints = getCurrentJoints(h).values.tolist()
    for i in range(NUMBER_OF_JOINTS):
        rad_pos = convertPosToRadPos(action[i])
        joints[THE_TESTED_JOINTS[i]] = rad_pos
    moving = "movej({0}, a=5.0, v=1.8)\n".format(joints)
    s.send(bytes(moving,'utf-8'))
    time.sleep(3)

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

for run_no in range(EPISODES):
    discrete_state = getStateDiscrete(getCurrentXYZ(HOST))
    goal_discrete = getStateDiscrete(GOAL)
    done = False

    while not done:
        if np.random.random() > epsilon:
            print("following the table")
            # get action from the Q-table
            # action = np.argmax(q_table[discrete_state])
            action =  np.unravel_index(np.argmax(q_table[discrete_state], axis=None), q_table[discrete_state].shape) #this will return a tuple of the position that has the highest value
        else: 
            # Get random action
            print("doing random")
            action = ()
            for x in range(NUMBER_OF_JOINTS):
                a = np.random.randint(0, NUMBER_ACTION)
                action = action + (a, )
        
        #taking action
        takeAction(action, s, HOST)

        new_XYZ = getCurrentXYZ(HOST)

        new_state_discrete = getStateDiscrete(new_XYZ)

        distance_goal = distanceInXYZ(new_XYZ, GOAL)

        reward = 1/distance_goal

        if distance_goal < ERROR_RATE:
            q_table[discrete_state + (action,)] = 1
            done = True
        else:
            # Maximum possible Q value in next step (for new state)
            max_future_q = np.max(q_table[new_state_discrete])

            # Current Q value (for current state and performed action)
            current_q = q_table[discrete_state + (action,)]

            # And here's our equation for a new Q value for current state and action
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

            # Update Q table with new Q value
            # Small notE: to access the position inside matrix you have to use tuple not array, that's why it is + (action, )
            q_table[discrete_state + (action,)] = new_q


        # Decaying is being done every episode if episode number is within decaying range
    epsilon -= epsilon_decay_value

    print("the running is ok for the run no:", run_no)
    print("epsilon is:", epsilon)

np.save(f"./qtableUR5e.npy", q_table)
s.close()