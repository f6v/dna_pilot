import uuid
import os
import io
from boto3 import session
from botocore.client import Config


REGION = "ams3"
ENDPOINT = "https://dna-pilot-files.ams3.digitaloceanspaces.com"
DO_ACCESS_ID = os.environ.get("DO_ACCESS_ID")
DO_SECRET_KEY = os.environ.get("DO_SECRET_KEY")


def get_client():
    do_session = session.Session()
    client = do_session.client(
        "s3",
        region_name=REGION,
        endpoint_url=ENDPOINT,
        aws_access_key_id=DO_ACCESS_ID,
        aws_secret_access_key=DO_SECRET_KEY,
    )

    return client


def save_vcf(file_obj):
    client = get_client()

    object_uid = str(uuid.uuid4())
    client.upload_fileobj(file_obj, "vcf", object_uid)

    return object_uid


def get_vcf(object_uid):
    client = get_client()

    vcf_obj = client.get_object(Bucket="vcf", Key=object_uid)
    vcf_content = vcf_obj["Body"].read().decode()

    return vcf_content
