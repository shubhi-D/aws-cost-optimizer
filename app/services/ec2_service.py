from app.config.aws_config import get_ec2_client

def get_running_instances():
    ec2 = get_ec2_client()

    response = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]},
                  {"Name": "tag:AutoStop", "Values": ["true"]}]

    )

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append({
                "InstanceId": instance["InstanceId"],
                "InstanceType": instance["InstanceType"],
                "LaunchTime": instance["LaunchTime"]
            })

    return instances


def stop_instances(instance_ids, dry_run=True):

    ec2 = get_ec2_client()

    if not instance_ids:
        print("No instances to stop")
        return

    print(f"Stopping instances: {instance_ids}")

    try:
        ec2.stop_instances(
            InstanceIds=instance_ids,
            DryRun=dry_run
        )

        if dry_run:
            print("Dry run successful — instances would be stopped")

    except Exception as e:
        if "DryRunOperation" in str(e):
            print("Dry run passed — permissions are correct")
        else:
            print(f"Error stopping instances: {e}")