
import traci
import rsu_mannager
import random
import math
import os
import sys
import xml.etree.ElementTree as ET
import numpy as np

from scipy.spatial import distance

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")

import sumolib
import traci

import RL_utils


def report_to_RSU(vehicle_list,threshold):

    count_RSU_messages = 0

    print 'start data reporting'
    #select vehicles to report to RSUs:
    #best_vehicles = get_all_vehicles(vehicle_list) #---w
    #best_vehicles = get_random_vehicles(vehicle_list) #---w
    best_vehicles = select_vehicles_by_threshold(vehicle_list,threshold) #---w

    for sender_vehicle in best_vehicles:   

        #print 'creating message'
        #message = create_message(sender_vehicle, vehicle_knowledge)
        
        #send district knowledge
        count_RSU_messages += 1 #--- overhead

    return count_RSU_messages




#---w
def get_random_vehicles(vehicle_list):
    
    vehicles=[]
    num_vehicles=random.choice(RL_utils.action_space)
    i=1
    while i <= num_vehicles:
        #print("***##:",vehicles_per_district[district_id])
        vehicle = random.choice(vehicle_list)
        vehicles.append(vehicle)
        i+=1
    
    return vehicles


#---w
def get_all_vehicles(vehicle_list):
   
    return vehicle_list

#---w
def select_vehicles_by_threshold(vehicle_list, threshold):
    print("*","threshold", threshold)
    selected_vehicles = []

    for vehicle in vehicle_list:
        neighbours = RL_utils.get_neighboring_vehicles(vehicle,vehicle_list)        
        num_neig = len(neighbours)
        if num_neig > threshold:
            selected_vehicles.append(vehicle)

    return selected_vehicles