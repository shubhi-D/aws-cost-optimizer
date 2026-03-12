from app.services.ec2_service import get_running_instances
from app.services.cloudwatch_service import get_cpu_utilization

IDLE_CPU_THRESHOLD = 5

def find_idle_instances():
    
    print("Starting find_idle_instances...")
    
    instances = get_running_instances()
    
    print(f"Found {len(instances)} running instances")
    
    if not instances:
        print("No instances found - check your AWS configuration or instances")
        return []

    idle_instances = []

    for instance in instances:
        instance_id = instance.get("InstanceId", "Unknown")
        print(f"Processing instance {instance_id}")
        
        try:
            cpu = get_cpu_utilization(instance["InstanceId"])
            print(f"Instance {instance_id} CPU avg: {cpu}")
            
            if cpu < IDLE_CPU_THRESHOLD:
                instance["avg_cpu"] = cpu
                idle_instances.append(instance)
                print(f"Instance {instance_id} marked as idle (CPU: {cpu})")
        except Exception as e:
            print(f"Error processing instance {instance_id}: {e}")

    print(f"Total idle instances found: {len(idle_instances)}")
    return idle_instances