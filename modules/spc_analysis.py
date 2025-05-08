#Statisical process control functions(charts, limits)
#Test Data
sim_data = [
    {'unit_id': 1001, 'step': 'Filling', 'time_step': 120.5, 'defected': False},
    {'unit_id': 1001, 'step': 'Capping', 'time_step': 130.7, 'defected': False},
    {'unit_id': 1001, 'step': 'Packaging', 'time_step': 150.0, 'defected': False},
]

def parse_simulation_data(sim_data):
    # Get raw data and sorts info based on:
    #{UID: , end_time: , is_defective: }

    #Function not defined yet
    unit_events = group_by_unit(sim_data)
    # Empty list that will hold all values
    parsed_listed = []

    for unit_id, events in sim_data:
        if not is_unit_complete(events):
            continue
        end_time = get_end_time(events)
        is_defective = check_if_defective(events)
        parsed_listed.append({
            'unit_id': unit_id,
            'end_time': end_time,
            'is_defective': is_defective
        })

    return parsed_listed

# Function that is grouping and sorting raw data by organizing them in appropriate dictionary
def group_by_unit(sim_data):
    uid_list = {}
    for event in sim_data:
        unit_id = event['unit_id']
        if unit_id not in uid_list:
            uid_list[unit_id] = []
        uid_list[unit_id].append(event)
    return uid_list

def is_unit_complete(sim_data):
    pass

#Function that gets the time for the last step in the product cycle
def get_end_time(sim_data):
    end_times = {}
    final_step = 'Packaging'
    for event in sim_data:
        id = event['unit_id']
        if event['step'] == final_step:
            end_times[id] = event['time_step']
    return end_times

# Function that checks if a product is defective
def check_if_defective(sim_data):
    for event in sim_data:
        if event['defected']:
            return True

#print(group_by_unit(sim_data))
print(get_end_time(sim_data))