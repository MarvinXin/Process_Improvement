#Statisical process control functions(charts, limits)
#Test Data
sim_data = [
    {'unit_id': 1001, 'step': 'Filling', 'time_step': 120.5, 'defected': False},
    {'unit_id': 1001, 'step': 'Capping', 'time_step': 130.7, 'defected': False},
    {'unit_id': 1001, 'step': 'Packaging', 'time_step': 150.0, 'defected': False},
    {'unit_id': 1002, 'step': 'Filling', 'time_step': 120.5, 'defected': False},
    {'unit_id': 1002, 'step': 'Capping', 'time_step': 130.7, 'defected': True},
    {'unit_id': 1002, 'step': 'Packaging', 'time_step': 150.0, 'defected': False},
]

def parse_simulation_data(sim_data):
    # Get raw data and sorts info based on:
    unit_events = group_by_unit(sim_data)

    # Empty lists that will hold all values
    good_units = []
    bad_units = []

    #Iterating through the dictionary and getting values for each value
    for unit_id, events in unit_events.items():
        end_time = get_end_time(events)
        is_defective = check_if_defective(events)

        # Dictionary format of what each items that will be used
        record = {
            'unit_id': unit_id,
            'end_time': end_time,
            'is_defective': is_defective
        }
        #Check to see if the unit is complete and appending it to appropriate list
        if is_unit_complete(events):
            good_units.append(record)
        else:
            bad_units.append(record)
    return good_units, bad_units

# Function that is grouping and sorting raw data by organizing them in appropriate dictionary
def group_by_unit(sim_data):
    uid_list = {}
    for event in sim_data:
        unit_id = event['unit_id']
        if unit_id not in uid_list:
            uid_list[unit_id] = []
        uid_list[unit_id].append(event)
    return uid_list



# Function to check if item is defective
def is_unit_complete(sim_data):
    for event in sim_data:
        if event['defected']:
            return False
    return True

#Function that gets the time for the last step in the product cycle
def get_end_time(sim_data):
   return max(event['time_step'] for event in sim_data)

# Function that checks if a product is defective
def check_if_defective(sim_data):
    for event in sim_data:
        if event['defected']:
            return True
    return False

result = parse_simulation_data(sim_data)
print(result)