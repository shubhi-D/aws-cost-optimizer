import streamlit as st
from app.services.ec2_service import get_running_instances
from app.utils.pricing import calculate_monthly_cost
from app.analyzers.idle_ec2_analyzer import find_idle_instances
from app.services.ec2_service import stop_instances

st.set_page_config(page_title="AWS Cost Optimizer", layout="wide")

st.title("AWS Cost Optimizer")
st.write("Detect and stop idle EC2 instances using CloudWatch metrics.")

st.header("Running EC2 Instances")

if st.button("Show Running Instances"):

    running_instances = get_running_instances()

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

        st.table(table_data)


def safe_round(value, decimals=2):
    if value is None:
        return 0.0
    return round(float(value), decimals)


# Scan button
if st.button("Scan for Idle Instances"):

    st.write("Scanning instances...")

    # store results in session state
    st.session_state["idle_instances"] = find_idle_instances()

# retrieve from session state
idle_instances = st.session_state.get("idle_instances", [])

if idle_instances:

    total_savings = sum(i.get("monthly_cost", 0) for i in idle_instances)

    st.metric("Potential Monthly Savings", f"${total_savings:.2f}")

    st.success(f"Found {len(idle_instances)} idle instances")

    table_data = []

    for inst in idle_instances:
        table_data.append({
            "Instance ID": inst["InstanceId"],
            "CPU": safe_round(inst.get("avg_cpu"), 2),
            "Network In": safe_round(inst.get("network_in"), 2),
            "Network Out": safe_round(inst.get("network_out"), 2),
            "Disk Read": safe_round(inst.get("disk_read_ops"), 2),
            "Disk Write": safe_round(inst.get("disk_write_ops"), 2),
            "Monthly Cost ($)": round(inst.get("monthly_cost", 0), 2),
        })

    st.table(table_data)

    if st.button("Stop Idle Instances"):

        ids = [i["InstanceId"] for i in idle_instances]

        stop_instances(ids, dry_run=False)

        st.warning("Stop command sent to AWS")

else:
    st.info("No idle instances found or scan not run yet.")