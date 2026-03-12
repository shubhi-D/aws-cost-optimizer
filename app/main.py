from app.analyzers.idle_ec2_analyzer import find_idle_instances
from app.services.ec2_service import stop_instances


def main():

    idle_instances = find_idle_instances()

    print(f"\nIdle Instances Found: {len(idle_instances)}")

    if not idle_instances:
        return

    instance_ids = [i["InstanceId"] for i in idle_instances]

    stop_instances(instance_ids, dry_run=False)


if __name__ == "__main__":
    main()