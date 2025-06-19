from modules.util import get_process_time
from modules.simulation import CycleTimes
import numpy as np

#perform basic Statstical process control


import numpy as np

import numpy as np

def calculate_ucl_lcl(values):
    if not values:
        return 0, 0, 0  # Nothing to calculate

    mean = np.mean(values)
    std_dev = np.std(values)
    ucl = mean + 3 * std_dev
    lcl = mean - 3 * std_dev
    return ucl, lcl, mean




def p_chart():
    pass

def defect_rate():
    pass

def calculate_mean_process_time(sim_data):
    data = get_process_time(sim_data)
    mean_time = 0
    for id, num in data.items():
        mean_time += num

    if len(data) > 0:
        return mean_time / len(data)
    else:
        return 0
    

def calculate_expected_process_time(cycle_times):
    return sum(cycle_times.values())

def mean(cycle_time):
    total_time = sum(cycle_time.values())
    mean_time = total_time / len(cycle_time)
    return mean_time

def subgrouping(data, subgroup_size=5):
    subgroups = []
    for i in range(0, len(data), subgroup_size):
        subgroup = data[i:i + subgroup_size]
        subgroups.append(subgroup)
    return subgroups


print(calculate_expected_process_time)