from app.config.aws_config import get_ec2_client

def get_running_instances():
    ec2 = get_ec2_client()

    response = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append({
                "InstanceId": instance["InstanceId"],
                "InstanceType": instance["InstanceType"]
            })

    return instances