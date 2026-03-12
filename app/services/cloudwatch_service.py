from datetime import datetime, timedelta
from app.config.aws_config import get_cloudwatch_client

def get_cpu_utilization(instance_id):

    cw = get_cloudwatch_client()

    end = datetime.utcnow()
    start = end - timedelta(minutes=15)

    metrics = cw.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[
            {"Name": "InstanceId", "Value": instance_id}
        ],
        StartTime=start,
        EndTime=end,
        Period=300,   # 5 minutes
        Statistics=["Average"]
    )

    datapoints = metrics["Datapoints"]

    print("Datapoints:", datapoints)   # debug

    if not datapoints:
        return None

    avg_cpu = sum(d["Average"] for d in datapoints) / len(datapoints)

    return avg_cpu