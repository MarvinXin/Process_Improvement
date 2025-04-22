# Main Simulation Logic (process flow, bottlenecks)

import random
import simpy


#Shift Parameters
workers = 8 # Number of workers
shift = 8 * 60 # 8 hours of work (in minutes)

#Machine Parameter
num_of_Machines = 4 #Number of machines
mean_time_to_make = 3000 # Mean Time to Failure (minutes)
repair_time = 240 # Repair Time (minutes)
break_mean = 1 / mean_time_to_make # How often the machines break respect to the mean_time_to_make
demands = 5000 #Quantity Quota for each day

#Process cycle times (in minutes per unit)
CycleTimes = {
    "Filling": 5 / 60,  
    "Capping" : 2 / 60, 
    "Labeling" : 3 / 60,
    "Packaging" : 6 / 60
}

#Process defect rates
DefectRates = {
    "Filling": 0.02,
    "Capping": 0.01,
    "Labeling": 0.015,
    "Packaging": 0.005
}

#Tracker for production output
total_production = 0
total_defects = 0


# Processing Units
def process_units(env, unit_id, machine, output_tracker):
    global total_defects, total_production