# Main Dashboard
from modules import run_simulation, parse_simulation_data, calculate_process_time, CycleTimes


#Testing out functionality
output_tracker, event_log = run_simulation()
#print(event_log)
#data = parse_simulation_data(event_log)
#print(output_tracker)
#print(data)

print(f'The process time is {calculate_process_time(CycleTimes)} minutes')
