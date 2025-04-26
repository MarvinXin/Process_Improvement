# Main Simulation Logic (process flow, bottlenecks)

import random
import simpy

random.seed(42)

#Shift Parameters
workers = 10  #Number of workers
hours = 8
shift = hours * 60 # 12 hours of work (in minutes)

#Machine Parameter
num_of_Machines = 10 #Number of machines
mean_time_to_make = 200 # Mean Time to Failure (minutes)
repair_time = 240 # Repair Time (minutes)
break_mean = 1 / mean_time_to_make # How often the machines break respect to the mean_time_to_make
demands = 5000 #Quantity Quota for each day

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

            if random.random() < DefectRates[step]:
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


    output_tracker = {
        'defects': 0,
        'produced': 0
    }

    # Start machine breakdown logic (MTBF/MTTR simulation)
    for machine in machines_resources:
        env.process(machine_breakdown(env, machine))  # Correct, runs for each individual machine

    for i in range(min(workers, num_of_Machines)):
        env.process(production_loop(env, i, machines_resources[i], workers_resources[i], output_tracker))
         
    #Run the simulation
    env.run(until=shift)
    
    return output_tracker


def production_loop(env, id, machines_resource, workers_resource, output_tracker, spawn_intervals=0.1, max_unit = None):
    units_created = 0
    while env.now < shift:
        if max_unit is not None and units_created >= max_unit:
            break

        env.process(process_units(env, id, machines_resource, workers_resource, output_tracker))
        yield env.timeout(spawn_intervals)

        id += 1
        units_created += 1

    

# Run the simulation
if __name__ == "__main__":
    results = run_simulation()
    print("\n=== Simulation Results ===")
    print(f"Produced units: {results['produced']}")
    print(f"Defective units: {results['defects']}")
    total = results['produced'] + results['defects']
    yield_rate = results['produced'] / total if total else 0

    print(f"Yield Rate: {yield_rate:.2%}")