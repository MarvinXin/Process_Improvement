
#Data processing
#Statistical process control functions(charts, limits)

#Test Data

#from .simulation import CycleTimes



import pandas as pd

def parse_simulation_data(sim_data):
    df = pd.DataFrame(sim_data)
    good_units = []
    bad_units = []
    unfinished_units = []

    # Group all events by unit_id
    unit_groups = df.groupby("unit_id")

    for unit_id, group in unit_groups:
        # Sort each unit's events in case they're out of order
        events = group.sort_values("time_step").to_dict(orient="records")

        process_time = get_process_time(events)
        is_defective = check_if_defective(events)
        is_complete = is_unit_complete(events)
        end_time_step = get_completion_time(events)

        record = {
            'unit_id': unit_id,
            'process_time': round(process_time, 2) if process_time is not None else None,
            'completion_time': round(end_time_step, 2) if end_time_step is not None else None,
            'is_defective': is_defective
        }

        if is_complete and not is_defective:
            good_units.append(record)
        elif is_complete and is_defective:
            bad_units.append(record)
        else:
            unfinished_units.append(record)

    return good_units, bad_units, unfinished_units



def is_unit_complete(sim_data):
    required_steps = {'Filling', 'Capping', 'Packaging'}  # adjust this to match your actual steps
    steps_done = set(event['step'] for event in sim_data)
    return required_steps.issubset(steps_done)


def get_process_time(sim_data):
    start = end = None
    for event in sim_data:
        if not isinstance(event, dict):
            print("Bad event:", event)
            continue  # Skip this bad input
        
        if event.get('step') == 'Filling' and start is None:
            start = event['time_step']
        elif event.get('step') == 'Packaging':
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


def get_completion_time(events):
    for event in events:
        if event['step'] == 'Packaging':
            return event['time_step']
    return None


def weighted_mean(events):
    pass