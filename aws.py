import logging
import boto3
from fastapi import HTTPException

logger = logging.getLogger(__name__)  # Provides the file name in the logging

s3 = boto3.client("s3")
bucket_name = "257288818923-engg-internship"
key = "modified_data.json"

try:
    response = s3.get_object(Bucket=bucket_name, Key=key)
    file_content = response["Body"].read().decode("utf-8")
    logger.info(f"Fetched {key} from {bucket_name}")
except Exception as e:
    logger.error(f"Failed to fetch {key} from {bucket_name}: {e}")  # Logs this error 
    raise HTTPException(
        status_code=500, detail="Failed to load dataset from S3") # Returns this exception to the user if data not present.