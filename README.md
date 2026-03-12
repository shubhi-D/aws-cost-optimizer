# AWS Cost Optimizer (Python)

A Python-based tool that detects idle EC2 instances using CloudWatch metrics to help reduce AWS infrastructure costs.

## Features

- Detects idle EC2 instances based on CPU utilization
- Uses AWS CloudWatch metrics
- Lists running EC2 instances automatically
- Outputs idle instance data in structured format
- Modular architecture for easy extension

## Tech Stack

- Python
- boto3
- AWS EC2
- AWS CloudWatch
- python-dotenv

## Project Structure

aws-cost-optimizer
│
├── app
│   ├── main.py
│   ├── config
│   ├── services
│   ├── analyzers
│   └── utils
│
├── output
├── requirements.txt
└── README.md

## How It Works

1. Fetch running EC2 instances
2. Query CloudWatch CPUUtilization metrics
3. Calculate average CPU usage
4. Mark instances with CPU < 5% as idle

## Example Output
Idle Instances Found: 2

InstanceId: i-002696b57775e40ee
InstanceType: t3.micro
Average CPU: 2.04%

InstanceId: i-06336d54d8937b73f
InstanceType: t2.micro
Average CPU: 3.85%


## Future Improvements

- Network usage detection
- Unused EBS volume detection
- Unattached Elastic IP detection
- Cost estimation
- Lambda automation