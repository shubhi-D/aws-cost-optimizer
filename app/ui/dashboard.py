import streamlit as st
import pandas as pd
import plotly.express as px

from app.services.ec2_service import get_running_instances
from app.services.ec2_service import stop_instances
from app.analyzers.idle_ec2_analyzer import find_idle_instances
from app.utils.pricing import calculate_monthly_cost


st.set_page_config(page_title="AWS Cost Optimizer", layout="wide")

st.title("🦇 AWS Cost Optimizer")
st.write("Detect and stop idle EC2 instances using CloudWatch metrics.")

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------

if "show_running" not in st.session_state:
    st.session_state.show_running = False

if "running_instances" not in st.session_state:
    st.session_state.running_instances = []

if "idle_instances" not in st.session_state:
    st.session_state.idle_instances = []


# -----------------------------
# RUNNING INSTANCES SECTION
# -----------------------------

st.header("Running EC2 Instances")

col1, col2 = st.columns(2)

with col1:
    if st.button("Show Running Instances"):
        st.session_state.show_running = True
        st.session_state.running_instances = get_running_instances()

with col2:
    if st.button("Hide Running Instances"):
        st.session_state.show_running = False


if st.session_state.show_running:

    running_instances = st.session_state.running_instances

    if not running_instances:
        st.info("No running instances found")

    else:

        table_data = []

        for inst in running_instances:

            table_data.append({
                "Instance ID": inst["InstanceId"],
                "Instance Type": inst["InstanceType"],
                "State": inst["State"],
                "Launch Time": inst["LaunchTime"],
                "Monthly Cost ($)": calculate_monthly_cost(inst["InstanceType"])
            })

        running_df = pd.DataFrame(table_data)

        st.table(running_df)


# -----------------------------
# IDLE INSTANCE SCAN
# -----------------------------

st.header("Idle EC2 Detection")

if st.button("Scan for Idle Instances"):

    st.write("Scanning instances...")

    st.session_state.idle_instances = find_idle_instances()


idle_instances = st.session_state.idle_instances


# -----------------------------
# DISPLAY RESULTS
# -----------------------------

if idle_instances:

    total_savings = sum(i.get("monthly_cost", 0) for i in idle_instances)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Potential Monthly Savings", f"${total_savings:.2f}")

    with col2:
        st.metric("Idle Instances Found", len(idle_instances))

    table_data = []

    for inst in idle_instances:

        table_data.append({
            "Instance ID": inst["InstanceId"],
            "CPU": round(inst.get("avg_cpu", 0), 2),
            "Network In": round(inst.get("network_in", 0), 2),
            "Network Out": round(inst.get("network_out", 0), 2),
            "Disk Read": round(inst.get("disk_read_ops", 0) or 0, 2),
            "Disk Write": round(inst.get("disk_write_ops", 0) or 0, 2),
            "Monthly Cost ($)": round(inst.get("monthly_cost", 0), 2)
        })

    df = pd.DataFrame(table_data)

    # -----------------------------
    # COST BAR CHART
    # -----------------------------

    st.subheader("Idle Instance Cost Distribution")

    st.bar_chart(
        df.set_index("Instance ID")["Monthly Cost ($)"]
    )

    # -----------------------------
    # PIE CHART COST SHARE
    # -----------------------------

    st.subheader("Cost Contribution per Instance")

    fig = px.pie(
        df,
        names="Instance ID",
        values="Monthly Cost ($)",
        title="Idle Instance Cost Share"
    )

    st.plotly_chart(fig)

    # -----------------------------
    # INSTANCE TABLE
    # -----------------------------

    st.subheader("Idle Instance Details")

    st.table(df)

    # -----------------------------
    # STOP INSTANCES BUTTON
    # -----------------------------

    if st.button("Stop Idle Instances"):

        ids = [i["InstanceId"] for i in idle_instances]

        stop_instances(ids, dry_run=False)

        st.warning("Stop command sent to AWS")


else:

    st.info("Run a scan to detect idle instances.")