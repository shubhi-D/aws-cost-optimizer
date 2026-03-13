import os
import boto3
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get AWS configuration from environment variables
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")  # Default to Mumbai region
AWS_PROFILE = os.getenv("AWS_PROFILE")

# Create boto3 session using profile
session = boto3.Session(profile_name=AWS_PROFILE)

def get_ec2_client():
    """
    Returns EC2 client using configured AWS profile and region
    """
    logger.info(f"Creating EC2 client for region: {AWS_REGION}")
    return session.client(
        "ec2",
        region_name=AWS_REGION
    )

def get_cloudwatch_client():
    """
    Returns CloudWatch client using configured AWS profile and region
    """
    logger.info(f"Creating CloudWatch client for region: {AWS_REGION}")
    return session.client(
        "cloudwatch",
        region_name=AWS_REGION
    )

def validate_region():
    """
    Validate that AWS_REGION is set and available
    """
    regions_to_try = [AWS_REGION, "ap-south-1", "us-east-1"]  # Try current, then Mumbai, then default
    
    for region in regions_to_try:
        try:
            test_session = boto3.Session()
            test_client = test_session.client("ec2", region_name=region)
            test_client.describe_regions()
            logger.info(f"Region {region} is available and accessible")
            return region
        except Exception as e:
            logger.warning(f"Region {region} not accessible: {e}")
            continue
    
    raise Exception("No accessible AWS regions found")