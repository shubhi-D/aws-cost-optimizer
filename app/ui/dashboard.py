import streamlit as st

from app.analyzers.idle_ec2_analyzer import find_idle_instances
from app.services.ec2_service import stop_instances

st.set_page_config(page_title="AWS Cost Optimizer", layout="wide")

st.title("AWS Cost Optimizer")

st.write("Detect and stop idle EC2 instances using CloudWatch metrics.")

def safe_round(value, decimals=2):
    """Safely round a value that might be None"""
    if value is None:
        return 0.0
    return round(float(value), decimals)

# scan button
if st.button("Scan for Idle Instances"):

    st.write("Scanning instances...")

    idle_instances = find_idle_instances()

    st.success(f"Found {len(idle_instances)} idle instances")

    if idle_instances:

        table_data = []

        for inst in idle_instances:
            table_data.append({
                "Instance ID": inst["InstanceId"],
                "CPU": safe_round(inst.get("avg_cpu"), 2),
                "Network In": safe_round(inst.get("network_in"), 2),
                "Network Out": safe_round(inst.get("network_out"), 2),
                "Disk Read": safe_round(inst.get("disk_read_ops"), 2),
                "Disk Write": safe_round(inst.get("disk_write_ops"), 2),
            })

        st.table(table_data)

        if st.button("Stop Idle Instances"):

            ids = [i["InstanceId"] for i in idle_instances]

            stop_instances(ids, dry_run=False)

            st.warning("Stop command sent to AWS")

    else:
        st.info("No idle instances found")