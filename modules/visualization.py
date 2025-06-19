#Visual graphics (matlib, seaborn, plotly)
from modules.spc_analysis import calculate_ucl_lcl
from modules.util import group_by_unit
import plotly.express as px
import streamlit as st


def plot_total_time_line(df, chart_key="total_time_chart"):
    df_sorted = df.sort_values("unit_id")
    """
    Line chart of total process time per unit.
    Expects df to have columns: 'unit_id', 'total_time'
    """
    fig = px.line(
        df_sorted,
        x='unit_id',
        y='process_time',
        title='Total Process Time per Unit',
        labels={'unit_id': 'Unit ID', 'process_time': 'Process Time (min)'}
    )
    return fig

def plot_spc_time_line(df, chart_key="SPC_time_chart"):
    df_sorted = df.sort_values("unit_id").reset_index(drop=True)
    
    # Assign each 5-unit chunk to a subgroup
    df_sorted["subgroup"] = (df_sorted.index // 5) + 1

    # Compute mean process time for each subgroup
    subgroup_means = df_sorted.groupby("subgroup")["process_time"].mean().reset_index()

    # Calculate control limits
    from modules.spc_analysis import calculate_ucl_lcl
    means_list = subgroup_means["process_time"].tolist()
    ucl, lcl, mean_time = calculate_ucl_lcl(means_list)
    centerline = sum(means_list) / len(means_list)

    # Add limits for plotting
    subgroup_means["UCL"] = ucl
    subgroup_means["LCL"] = lcl
    subgroup_means["Centerline"] = centerline

    # Plot using plotly
    import plotly.graph_objects as go
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=subgroup_means["subgroup"],
        y=subgroup_means["process_time"],
        mode="lines+markers",
        name="Subgroup Mean",
        line=dict(color="white")
    ))

    fig.add_trace(go.Scatter(
        x=subgroup_means["subgroup"],
        y=subgroup_means["UCL"],
        mode="lines",
        name="UCL",
        line=dict(color="red", dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=subgroup_means["subgroup"],
        y=subgroup_means["LCL"],
        mode="lines",
        name="LCL",
        line=dict(color="blue", dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=subgroup_means["subgroup"],
        y=subgroup_means["Centerline"],
        mode="lines",
        name="Centerline",
        line=dict(color="green", dash="dot")
    ))

    fig.update_layout(
        title="SPC Chart - Mean Process Time per Subgroup",
        xaxis_title="Subgroup",
        yaxis_title="Mean Process Time (min)"
    )

    import streamlit as st
    st.plotly_chart(fig, key=chart_key, use_container_width=True)

    return fig
