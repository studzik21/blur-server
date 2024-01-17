import os
import boto3
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_ACCESS_SECRET = os.environ.get("AWS_ACCESS_SECRET")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_FOLDER_NAME = os.environ.get("S3_FOLDER_NAME")
S3_BUCKET_BASE_URL = os.environ.get("S3_BUCKET_BASE_URL")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_ACCESS_SECRET,
    aws_session_token=AWS_SESSION_TOKEN
)

def rename_file(filename: str):
    """
    Rename a file using its original name (modified) and current timestamp
    """
    uploaded_date = datetime.utcnow()

    if filename is None:
        raise ValueError("Filename is required")

    splitted = filename.rsplit(".", 1)
    if len(splitted) < 2:
        raise ValueError("Filename must have an extension")

    updated_filename = splitted[0]
    file_extension = splitted[1]

    # Combining filename and timestamp
    updated_filename = f"{S3_FOLDER_NAME}/{updated_filename}-{uploaded_date.strftime('%Y%m%d%H%M%S')}"

    # Combining the updated filename and file extension
    updated_filename = f"{updated_filename}.{file_extension}"

    return updated_filename

def get_url(filename):
    return f"{S3_BUCKET_BASE_URL}/{filename}"

def upload_file_to_s3(path, filename) -> str:
    """
    Upload file using normal synchronous way
    """
    s3.upload_file(
        path,
        S3_BUCKET_NAME,
        filename,
    )
