from modules.util import get_process_time
from modules.simulation import CycleTimes
import numpy as np

#perform basic Statstical process control


def calculate_ucl_lcl():
    pass

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
    pass

def mean(cycle_time):
    total_time = 0
    for step in cycle_time.keys():
        total_time += cycle_time[step]

    mean_time = total_time / len(cycle_time)
    return mean_time