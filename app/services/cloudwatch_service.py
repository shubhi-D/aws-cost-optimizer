from datetime import datetime, timedelta


def get_metric_average(cw, instance_id, metric_name, statistic="Average"):

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


def get_cpu_utilization(cw, instance_id):
    return get_metric_average(
        cw,
        instance_id,
        "CPUUtilization",
        "Average"
    )