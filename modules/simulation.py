# Main Simulation Logic (process flow, bottlenecks)

import random
import simpy


#Shift Parameters
workers = 8 # Number of workers
shift = workers * 60 # 8 hours of work per workers (in minutes)

#Machine Parameter
num_of_Machines = 4 #Number of machines
mean_time_to_make = 3000 # Mean Time to Failure (minutes)
repair_time = 240 # Repair Time (minutes)
break_mean = 1 / 2 # How often the machines break respect to the mean_time_to_make
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



# Processing Units functions
def process_units(env, unit_id, machine, output_tracker):

    for step, cycle_time in CycleTimes.items():
        with machine.request() as req:
            yield req
            yield env.timeout(cycle_time)

            if random.random() < DefectRates[step]:
                output_tracker['defects'] += 1
                return
            
    output_tracker['produced'] += 1

# Machine Breaking functions
def machine_breakdown(env, machine):
    while True:
        yield env.timeout(random.expovariate(break_mean))
        with machine.request() as req:
            yield req
            print(f"[{env.now:.2f}] Machine broke down!")
            yield env.timeout(repair_time)
            print(f"[{env.now:.2f}] Machine repaired.")


# Run the simulation function
def run_simulation():
    env = simpy.Environment()
    machine = simpy.Resource(env, capacity=num_of_Machines)
    output_tracker = {
        'defects': 0,
        'produced': 0
    }

    #Start Machine_Breakdown process if any
    env.process(machine_breakdown(env, machine))


    #Simulate the continuous production
    item_id = 0
    def generate_units(env):
        nonlocal item_id
        while env.now < shift:
            env.process(process_units(env, item_id, machine, output_tracker))
            yield env.timeout(0.2)
            item_id += 1

    env.process(generate_units(env))
    env.run(until=shift)
    
    return output_tracker

# Run the simulation
if __name__ == "__main__":
    results = run_simulation()
    print("\n=== Simulation Results ===")
    print(f"Produced units: {results['produced']}")
    print(f"Defective units: {results['defects']}")