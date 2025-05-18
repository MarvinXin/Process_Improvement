
#Data processing
#Statistical process control functions(charts, limits)

#Test Data

#from .simulation import CycleTimes

sample_data = [
    # Good units (complete and no defects)
    {'unit_id': 1, 'step': 'Filling', 'time_step': 10.0, 'defected': False},
    {'unit_id': 1, 'step': 'Capping', 'time_step': 15.0, 'defected': False},
    {'unit_id': 1, 'step': 'Packaging', 'time_step': 30.0, 'defected': False},
    
    # Bad units (complete but defective)
    {'unit_id': 2, 'step': 'Filling', 'time_step': 12.0, 'defected': False},
    {'unit_id': 2, 'step': 'Capping', 'time_step': 18.0, 'defected': True},  # defect here
    {'unit_id': 2, 'step': 'Packaging', 'time_step': 35.0, 'defected': False},
    
    # Unfinished units (incomplete)
    {'unit_id': 3, 'step': 'Filling', 'time_step': 11.0, 'defected': False},
    {'unit_id': 3, 'step': 'Capping', 'time_step': 17.0, 'defected': False},
    # Missing Packaging step
    
    # Another bad unit (complete but defective)
    {'unit_id': 4, 'step': 'Filling', 'time_step': 14.0, 'defected': False},
    {'unit_id': 4, 'step': 'Capping', 'time_step': 19.0, 'defected': False},
    {'unit_id': 4, 'step': 'Packaging', 'time_step': 33.0, 'defected': True},  # defect here
]



def parse_simulation_data(sim_data):
    unit_events = group_by_unit(sim_data)
    good_units = []
    bad_units = []
    unfinished_units = []

    for unit_id, events in unit_events.items():
        process_time = get_process_time(events)
        is_defective = check_if_defective(events)
        is_complete = is_unit_complete(events)

        record = {
            'unit_id': unit_id,
            'process_time': process_time,
            'is_defective': is_defective
        }

        if is_complete and not is_defective:
            good_units.append(record)
        elif is_complete and is_defective:
            bad_units.append(record)
        else:
            unfinished_units.append(record)


    return good_units, bad_units, unfinished_units



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
    required_steps = {'Filling', 'Capping', 'Packaging'}  # adjust this to match your actual steps
    steps_done = set(event['step'] for event in sim_data)
    return required_steps.issubset(steps_done)


#Function that gets the time for the last step in the product cycle
def get_process_time(sim_data):
    start = end = None
    for event in sim_data:
        if event['step'] == 'Filling' and start is None:
            start = event['time_step']
        elif event['step'] == 'Packaging':
            end = event['time_step']
    
    if start is not None and end is not None:
        return end - start
    else:
        return None


# Function that checks if a product is defective
def check_if_defective(sim_data):
    for event in sim_data:
        if event['defected']:
            return True
    return False



print(parse_simulation_data(sample_data))
