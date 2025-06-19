# Main Simulation Logic (process flow, bottlenecks)

import random
import simpy


random.seed(42)

#Shift Parameters
workers = 3  #Number of workers

shift = 480 # 12 hours of work (in minutes)

#Machine Parameter
num_of_Machines = 3 #Number of machines
mean_time_to_make = 200 # Mean Time to Failure (minutes)
repair_time = 120 # Repair Time (minutes)
break_mean = 1 / mean_time_to_make # How often the machines break respect to the mean_time_to_make
demands = 5000 # Quantity Quota for each day
event_log = [] # Event list to used to the spc_analysis

#Process cycle times (in minutes per unit)
CycleTimes = {
    "Filling": 10 / 60,  
    "Capping" : 5 / 60, 
    "Labeling" : 5 / 60,
    "Packaging" : 15 / 60
}

#Process defect rates
DefectRates = {
    "Filling": 0.02, #% of Defect at filling station
    "Capping": 0.01, #% of Capping at filling station
    "Labeling": 0.04, #% of Labeling at filling station
    "Packaging": 0.03 #% of Packaging at filling station
}



# Processing Units functions
def process_units(env, unit_id, machine, worker, output_tracker):
    for step, cycle_time in CycleTimes.items():
        with machine.request() as m_req, worker.request() as w_req:
            yield m_req & w_req
            #print(f"[{env.now:.2f}] Unit {unit_id} starting {step} with cycle time {cycle_time}.")
            yield env.timeout(cycle_time)
            
            #Determine if the product is defected
            defected = random.random() < DefectRates[step]

            
            
            
            #Logging events into event_list
            event_log.append({
                'unit_id': unit_id,
                'step': step,
                'time_step': env.now,
                'defected': defected
            })

            #Checks to see if the item is defected
            if defected:
                output_tracker['defects'] += 1
                #print(f"[{env.now:.2f}] Unit {unit_id} defected at {step}.")

                return
            
    output_tracker['produced'] += 1
    #print(f"[{env.now:.2f}] Unit {unit_id} successfully produced.")


# Machine Breaking functions
def machine_breakdown(env, machine):
    while True:
        yield env.timeout(random.expovariate(break_mean))
        with machine.request() as req:
            yield req
            #print(f"[{env.now:.2f}] Machine broke down!")
            yield env.timeout(repair_time)
            #print(f"[{env.now:.2f}] Machine repaired.")


# Run the simulation function
def run_simulation():
    env = simpy.Environment()

    workers_resources = [simpy.Resource(env, capacity=1) for _ in range(workers)]  # Correct
    machines_resources = [simpy.Resource(env, capacity=1) for _ in range(num_of_Machines)]  # Correct


    output_tracker = [{'defects': 0, 'produced': 0} for _ in range (num_of_Machines)]

    # Start machine breakdown logic (MTBF/MTTR simulation)
    for machine in machines_resources:
        env.process(machine_breakdown(env, machine))  # Correct, runs for each individual machine

    for i in range(min(workers, num_of_Machines)):
        env.process(production_loop(env, i, machines_resources[i], workers_resources[i], output_tracker[i]))
         
    #Run the simulation
    print(f"Running simulation for {shift} minutes...")
    env.run(until=shift)
    
    return output_tracker, event_log


def production_loop(env, id, machines_resource, workers_resource, output_tracker, spawn_intervals=1, max_unit = None):
    units_created = 0
    while env.now < shift:
        if max_unit is not None and units_created >= max_unit:
            break
        
        #Creating a new unit process
        env.process(process_units(env, id, machines_resource, workers_resource, output_tracker))

        #Wait a certain amount of time before starting again
        yield env.timeout(spawn_intervals)

        id += 1
        units_created += 1

    

# Run the simulation
if __name__ == "__main__":

    results = run_simulation()

'''    print("\n=== Simulation Results ===")

    total_produced = total_defects = 0

    for i, r in enumerate(results):
        total = r['produced'] + r['defects']
        yield_rate = r['produced'] / total if total else 0
        print(f"Machine {i+1}: Produced: {r['produced']}, Defective: {r['defects']}, Yield: {yield_rate:.2%}")
        total_produced += r['produced']
        total_defects += r['defects']

    total = total_produced + total_defects
    overall_yield = total_produced / total if total else 0
    print("\n=== Overall Totals ===")
    print(f"Produced units: {total_produced}")
    print(f"Defective units: {total_defects}")
    print(f"Overall Yield Rate: {overall_yield:.2%}")'''


