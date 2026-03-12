import os
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_PROFILE = os.getenv("AWS_PROFILE")

# Create boto3 session using profile
session = boto3.Session(profile_name=AWS_PROFILE)

def get_ec2_client():
    """
    Returns EC2 client using configured AWS profile and region
    """
    return session.client(
        "ec2",
        region_name=AWS_REGION
    )

def get_cloudwatch_client():
    """
    Returns CloudWatch client using configured AWS profile and region
    """
    return session.client(
        "cloudwatch",
        region_name=AWS_REGION
    )