#Statisical process control functions(charts, limits😂

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


def group_by_unit(sim_data):
    pass

def is_unit_complete(sim_data):
    pass

def get_end_time(sim_data):
    pass

def check_if_defective(events):
    pass