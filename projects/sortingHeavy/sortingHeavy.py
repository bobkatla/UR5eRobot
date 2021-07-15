# This is a simple project using reinforcement learning (Q-learning) to sort the given object

# import sys
# sys.path.append("..") # So it is posible to acceess the commonSources
# import commonSources.moving.test as holding
# print(holding.a)

# Import needed libs
import numpy as np 
import subprocess
import math

# There will be 2 baskets, each is corresponding to a position (hence, the movements are fixed)
basket_heavy = []
basket_light = []

# Some constants
picking_pos_up = []
picking_pos_down = []
measuring_pos = []

PI = math.pi

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 1000

NUMBER_ACTION = 2 # This is corresponding to the number of basket
NUMBER_OBJECT = 2
DISCRETE_SIZE = [NUMBER_OBJECT, NUMBER_ACTION ] #NOTE: objects are the rows while actions are the col
# Here will be the functiosn wrapper

def load_gripper():
    # This function just to load the gripper script
    #set up the functions for gripper
    f = open ("../commonSources/Gripper.script", "rb")   #Robotiq Gripper
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)

def custom_command(the_command_file_pos:str) -> str:
    # This is just a function to create the custom command to send to the robot
    # The input file (input is the pos of the file) would be .txt
    f = open(the_command_file_pos, "r")
    l = f.read()
    return l

custom_command("./customCommand.txt")

def move_to(pos):
    # Move to a point
    NotImplemented

def pick_up():
    # The pos to pick up
    NotImplemented

def put_in_basket(basket):
    # The pos to put in basket
    NotImplemented

def searching_to_grasp():
    # A main func to search for the grasp object
    NotImplemented

def identify_object() -> []:
    # Measure to know whether what type of object is it based on the force
    NotImplemented

def measure_force(joint_number:int) -> int:
    # Measure the force on the corresponding joint
    NotImplemented



# Set up the tabular storing for Q value to update
start_q_table = None

# create the table with the size
if start_q_table is None:
    q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_SIZE))
    
else: 
    # q_table = np.load(f"./qtableUR5e.npy")
    q_table = np.load(f"./qtableTested.npy")


# Move to a 
def main():
    # Exploration settings
    epsilon = 0  # not a constant, going to be decayed
    epsilon_decay_value = 1/EPISODES

    for run_no in range(EPISODES):
        discrete_state = getStateDiscrete(getCurrentXYZ(HOST))
        # goal_discrete = getStateDiscrete(GOAL)
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
                q_table[discrete_state + (action,)] = 100
                print("reached goal")
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

        print("the running is ok for the episode:", run_no)
        print("epsilon will now be:", epsilon)

    np.save(f"./qtableUR5e.npy", q_table)
    s.close()
