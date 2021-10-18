import ql_agent
import server_utilization
import substrate_graph
import networkx as nx
from networkx.readwrite import json_graph
from scipy.spatial import distance
import random

import traci
import numpy as np

#reporting_interval: cada cuanto se realiza un data reporting/agente decide nuevo threshold

action_space = [i for i in range(51)]
n_actions = len(action_space)

variable_size = 11 # num of possible values each variable can take
n_state_variables = 2 #3 # num of variables in a state
n_states = variable_size**n_state_variables

end_sim_time = 86000
reporting_interval = 20 #40 #20 
num_episodes = 100 #50
num_steps = int(end_sim_time/num_episodes/reporting_interval)

communication_range = 300

#normalization values:
max_speed = 13.9 #max allowed speed
max_num_vehicles = 404 #179

def get_reward(num_messages):
    '''
    tr: response time
    tre: max time to execute rerouting task again
    tproc: processing time
    tprop: propagation time
    '''
    overhead = num_messages
    #print("**",type(overhead))
    reward = float(overhead)/max_num_vehicles
    #print("**",reward)
    return reward


def get_state(vehicle_list, graph):
    
    mean_speed = get_mean_speed(graph)
    print("mean_speed:", mean_speed)
    #mean_neighbours = get_mean_neighbours(vehicle_list)
    #print("mean_neighbours:", mean_neighbours)
    total_vehicles = get_total_vehicles()
    print("total_vehicles:", total_vehicles)
    #print("*",[mean_speed/max_speed, mean_neighbours/max_num_vehicles, total_vehicles/max_num_vehicles])
    #state_ = [round(mean_speed/max_speed,1), round(mean_neighbours/max_num_vehicles,1), round(total_vehicles/max_num_vehicles,1)]
    state_ = [round(mean_speed/max_speed,1)*10, round(total_vehicles/max_num_vehicles,1)*10]
    print("state_",state_)
    state = translateStateToIndex(state_)
    print("state:",state)
    return state
             

def translateStateToIndex(state):
    '''
    returns state index from a given state
    '''
    #index = state[0]*(variable_size**2) + state[1]*variable_size + state[2]
    print("*translateStateToIndex:",state[0],state[1])
    index = state[0]*variable_size + state[1]
    return int(index)


def get_mean_speed(graph):
    mean_speeds =[]
    for road in graph.nodes_iter():
        last_mean_speed = traci.edge.getLastStepMeanSpeed(road)
        #print("last_mean_speed:",last_mean_speed)
        mean_speeds.append(last_mean_speed)
    return np.mean(mean_speeds)



def get_mean_neighbours(vehicle_list):
    num_neighbours_list = []
    for vehicle in vehicle_list:
        num_neighbours = len(get_neighboring_vehicles(vehicle,vehicle_list))
        num_neighbours_list.append(num_neighbours)

    return np.mean(num_neighbours_list)

def get_total_vehicles():
    return float(len(traci.vehicle.getIDList()))


def get_neighboring_vehicles(vehicle, vehicle_list):

    neighboring_vehicles = []
    vehicle_position = traci.vehicle.getPosition(vehicle)

    for neighbor in vehicle_list:
        if neighbor == vehicle:
            continue

        neighbor_position = traci.vehicle.getPosition(neighbor)
        distance2vehicle = distance.euclidean(vehicle_position, neighbor_position)

        if distance2vehicle <= communication_range:
            neighboring_vehicles.append(neighbor)

    return neighboring_vehicles


# utilizations = get_nodes_utilizations()
# print("utilizations:", utilizations)
# #print("state utilizations:",build_state(utilizations))
# #print("state index:",translateStateToIndex(build_state(utilizations)))

# vehicle_loc = [500,1200] #get vehicle location from traci
# distances = get_nodes_distances(vehicle_loc)
# print("distances:",distances)
# #print("state:",build_state(distances))
# #print("state index:",translateStateToIndex(build_state(distances)))

# print("state:", build_state(utilizations,distances))
# print("state:", translateStateToIndex(build_state(utilizations,distances)))
# print("state:", translateStateToIndex([0,0,0,0,0]))
# print("state:", translateStateToIndex([20,20,20,20,20]))

#0,1,2,3,4
#state_list_ = [80+40,40+90,90+40,60+70,40+90] #max= 200

#state_list = [0.6,0.65,0.65,0.65,0.65] 
             #[] 



#state_list_ = [60+60, 50+30, 40+90, 70+60, 40+90]
#state_list = [0.6,0.65,0.65,0.65,0.65]#12


#state_list_ = [2+3, 5+1, 4+1, 3+2, 4+4]
#state_list = [6,6,5,5,8]






 