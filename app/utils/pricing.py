EC2_PRICING = {
    "t2.micro": 0.0116,
    "t3.micro": 0.0104,
    "t3.small": 0.0208,
    "t3.medium": 0.0416
}

def calculate_monthly_cost(instance_type):

    hourly = EC2_PRICING.get(instance_type, 0)

    monthly = hourly * 24 * 30

    return round(monthly, 2)