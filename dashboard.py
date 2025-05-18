# Main Dashboard
from modules import run_simulation, parse_simulation_data, calculate_expected_process_time, calculate_mean_process_time, calculate_ucl_lcl

output, data = run_simulation()
good_units, bad_units, unfinished = parse_simulation_data(data)
#print(good_units)
print(good_units)

'''
# --- Sample Input Data --
CycleTimes = {
    "Filling": 10 / 60,
    "Capping": 5 / 60,
    "Labeling": 5 / 60,
    "Packaging": 15 / 60,
}

sim_data = [
    {'unit_id': 1001, 'step': 'Filling', 'time_step': 115.0},
    {'unit_id': 1001, 'step': 'Packaging', 'time_step': 150.0},
    {'unit_id': 1002, 'step': 'Filling', 'time_step': 200.0},
    {'unit_id': 1002, 'step': 'Packaging', 'time_step': 230.0},
    {'unit_id': 1003, 'step': 'Filling', 'time_step': 300.0},
    {'unit_id': 1003, 'step': 'Packaging', 'time_step': 330.0},
]


#print(f'The process time is {calculate_process_time(CycleTimes)} minutes')

actual_mean = calculate_mean_process_time(sim_data)
expected_mean = calculate_expected_process_time(CycleTimes)
ucl, lcl = calculate_ucl_lcl(sim_data)

print(f"Actual Mean Process Time: {actual_mean:.2f} minutes ")
print(f"Expected Mean Process Time: {expected_mean:.2f} minutes")
print(f"UCL:, {ucl:.2f} minutes")
print(f"LCL:, {lcl:.2f} minutes")'''

