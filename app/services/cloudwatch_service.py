from datetime import datetime, timedelta
from app.config.aws_config import get_cloudwatch_client


def get_metric_average(instance_id, metric_name, statistic="Average"):

    cw = get_cloudwatch_client()

    end = datetime.utcnow()
    start = end - timedelta(minutes=15)

    metrics = cw.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[
            {"Name": "InstanceId", "Value": instance_id}
        ],
        StartTime=start,
        EndTime=end,
        Period=300,   # 5 minutes
        Statistics=[statistic]
    )

    datapoints = metrics["Datapoints"]

    print(f"{metric_name} datapoints:", datapoints)

    if not datapoints:
        return None

    avg_value = sum(d[statistic] for d in datapoints) / len(datapoints)

    return avg_value


def get_cpu_utilization(instance_id):
    return get_metric_average(
        instance_id,
        "CPUUtilization",
        "Average"
    )