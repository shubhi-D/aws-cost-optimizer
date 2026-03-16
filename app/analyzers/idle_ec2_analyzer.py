from app.services.ec2_service import get_running_instances
from app.services.cloudwatch_service import get_cpu_utilization, get_metric_average
from app.config.aws_config import AWS_REGION, validate_region, get_cloudwatch_client
from datetime import datetime, timezone
from app.utils.pricing import calculate_monthly_cost
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IDLE_CPU_THRESHOLD = 5
NETWORK_IN_THRESHOLD = 5000000
NETWORK_OUT_THRESHOLD = 5000000
DISK_READ_THRESHOLD = 5
DISK_WRITE_THRESHOLD = 5

# Minimum age before evaluating instance
MIN_INSTANCE_AGE_MINUTES = 2


def find_idle_instances():

    print("Starting find_idle_instances...")

    # Validate AWS region access first
    try:
        verified_region = validate_region()
        print(f"Successfully connected to AWS region: {verified_region}")
    except Exception as e:
        print(f"AWS region validation failed: {e}")
        return []

    # Create ONE CloudWatch client
    cw = get_cloudwatch_client()

    # Show effective region being used
    print(f"Using AWS region: {AWS_REGION}")

    instances = get_running_instances()

    print(f"Found {len(instances)} running instances")

    if not instances:
        print("No instances found - check your AWS configuration or instances")
        print("Possible issues:")
        print("- No running instances with AutoStop=true tag in this region")
        print("- AWS credentials or permissions issue")
        print(f"- Region mismatch: Code is searching in {AWS_REGION}")
        return []

    idle_instances = []

    for instance in instances:

        instance_id = instance.get("InstanceId", "Unknown")
        launch_time = instance.get("LaunchTime")

        print(f"Processing instance {instance_id}")

        try:

            # ---------- Instance Age Filter ----------

            if launch_time:
                age_minutes = (
                    datetime.now(timezone.utc) - launch_time
                ).total_seconds() / 60

                if age_minutes < MIN_INSTANCE_AGE_MINUTES:
                    print(
                        f"Skipping {instance_id} (instance too new: {age_minutes:.1f} minutes old)"
                    )
                    continue

            # ---------- CPU Duration Validation ----------

            cpu_points = get_cpu_utilization(cw, instance_id)

            if cpu_points is None:
                print(f"No CPU metrics yet for {instance_id}, skipping")
                continue

            cpu_idle = all(p["Average"] < IDLE_CPU_THRESHOLD for p in cpu_points)

            # ---------- Other Metrics (Average based) ----------

            network_in = get_metric_average(cw, instance_id, "NetworkIn")
            network_out = get_metric_average(cw, instance_id, "NetworkOut")

            disk_read = get_metric_average(cw, instance_id, "DiskReadOps")
            disk_write = get_metric_average(cw, instance_id, "DiskWriteOps")

            print(
                f"{instance_id} metrics -> "
                f"CPU_points:{cpu_points}, NetIn:{network_in}, NetOut:{network_out}, "
                f"DiskRead:{disk_read}, DiskWrite:{disk_write}"
            )

            print(
                f"Checks -> "
                f"CPU_idle:{cpu_idle}, "
                f"NetIn:{network_in is None or network_in < NETWORK_IN_THRESHOLD}, "
                f"NetOut:{network_out is None or network_out < NETWORK_OUT_THRESHOLD}, "
                f"DiskRead:{disk_read is None or disk_read < DISK_READ_THRESHOLD}, "
                f"DiskWrite:{disk_write is None or disk_write < DISK_WRITE_THRESHOLD}"
            )

            # ---------- Idle Decision ----------

            if (
                cpu_idle
                and (network_in is None or network_in < NETWORK_IN_THRESHOLD)
                and (network_out is None or network_out < NETWORK_OUT_THRESHOLD)
                and (disk_read is None or disk_read < DISK_READ_THRESHOLD)
                and (disk_write is None or disk_write < DISK_WRITE_THRESHOLD)
            ):

                instance["cpu_datapoints"] = cpu_points
                instance["network_in"] = network_in
                instance["network_out"] = network_out
                instance["disk_read_ops"] = disk_read
                instance["disk_write_ops"] = disk_write
                instance["monthly_cost"] = calculate_monthly_cost(instance["InstanceType"])

                idle_instances.append(instance)

                print(f"Instance {instance_id} marked as idle")

        except Exception as e:
            print(f"Error processing instance {instance_id}: {e}")

    print(f"Total idle instances found: {len(idle_instances)}")

    return idle_instances