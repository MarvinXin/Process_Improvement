# Main Dashboard
from modules import run_simulation, parse_simulation_data, plot_total_time_line, plot_spc_time_line
import pandas as pd
import streamlit as st





output, data = run_simulation()
good_units, bad_units, unfinished = parse_simulation_data(data)
#print(good_units)


df = pd.DataFrame(good_units)

unit_summary = df.sort_values("unit_id")
unit_summary.rename(columns={"process_time": "process_time"}, inplace=True)
unit_summary = unit_summary.sort_values("unit_id")

fig = plot_total_time_line(df)
st.plotly_chart(fig, key="main_chart")
plot_spc_time_line(df)