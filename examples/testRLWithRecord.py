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
EPISODES = 25000
NUMBER_ACTION = 6
REWARD_ARR = 1
PELNATY = -1

DISCRETE_OS_SIZE = [20,20,20]
a = 2
discrete_os_win_size = 2/20

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [NUMBER_ACTION]))

# Exploration settings
epsilon = 1  # not a constant, going to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

# setup functions
def takeAction(rad_pos, joint_index, s, h):
    joints = getCurrentJoints(h).values.tolist()
    joints[joint_index] = rad_pos
    moving = "movej({0}, a=2.0, v=0.8)\n".format(joints)
    s.send(bytes(moving,'utf-8'))
    time.sleep(1)

def getTablePos(h):

    print("will fill up")

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

def getCurrentJoints(h):
    # getting the current position of each joint of the robot
    subprocess.check_output(["python", "record.py", "--host", str(h), "--samples", "1", "--frequency", "5", "--config", "curQ_record_config.xml"])
    # test2 = str(result_joints)
    # print(test2)
    c = pd.read_csv("./robot_data.csv")
    actual_joints = c.loc[0,:]
    # print(d)

    return actual_joints

#set up the connection

# HOST = "10.10.10.7"
HOST = "127.0.0.1"

PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("connection done\n")

# #moving
# Q0 = [0,PI/-2,0,PI/-2,0,0]
# Q1 = [-1.95, -1.66, 1.71, -1.62, -1.56, 1.19]
# Q3 = [1.3, -0.16, 0.54, -1.94, -1.47, 0.16]

# moveQ0 = "movej({0}, a=2.0, v=0.8)\n".format(Q0)
# moveQ1 = "movej({0}, a=2.0, v=0.8)\n".format(Q1)
# moveQ3 = "movej({0}, a=2.0, v=0.8)\n".format(Q3)

# s.send(bytes(moveQ0,'utf-8'))
# time.sleep(1)

# print(len(q_table))

test = getCurrentJoints(HOST).values.tolist()
print(test[0])

s.close()
'''
SHOW_EVERY = 3000


def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low)/discrete_os_win_size
    return tuple(discrete_state.astype(np.int))  # we use this tuple to look up the 3 Q values for the available actions in the q-table


for episode in range(EPISODES):
    discrete_state = get_discrete_state(env.reset())
    done = False

    if episode % SHOW_EVERY == 0:
        render = True
        print(episode)
    else:
        render = False

    while not done:

        if np.random.random() > epsilon:
            # Get action from Q table
            action = np.argmax(q_table[discrete_state])
        else:
            # Get random action
            action = np.random.randint(0, env.action_space.n)


        new_state, reward, done, _ = env.step(action)

        new_discrete_state = get_discrete_state(new_state)

        if episode % SHOW_EVERY == 0:
            print("sup")
        #new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        # If simulation did not end yet after last step - update Q table
        if not done:

            # Maximum possible Q value in next step (for new state)
            max_future_q = np.max(q_table[new_discrete_state])

            # Current Q value (for current state and performed action)
            current_q = q_table[discrete_state + (action,)]

            # And here's our equation for a new Q value for current state and action
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

            # Update Q table with new Q value
            q_table[discrete_state + (action,)] = new_q


        # Simulation ended (for any reson) - if goal position is achived - update Q value with reward directly
        elif new_state[0] >= env.goal_position:
            #q_table[discrete_state + (action,)] = reward
            q_table[discrete_state + (action,)] = 0

        discrete_state = new_discrete_state

    # Decaying is being done every episode if episode number is within decaying range
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        epsilon -= epsilon_decay_value
'''