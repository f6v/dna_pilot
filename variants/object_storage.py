import uuid
import os
import io
from boto3 import session
from botocore.client import Config


REGION = 'ams3'
BUCKET = 'https://dna-pilot-files.ams3.digitaloceanspaces.com'
DO_ACCESS_ID = os.environ.get('DO_ACCESS_ID')
DO_SECRET_KEY = os.environ.get('DO_SECRET_KEY')

def get_client():
    do_session = session.Session()
    client = do_session.client('s3',
                                region_name=REGION,
                                endpoint_url=BUCKET,
                                aws_access_key_id=DO_ACCESS_ID,
                                aws_secret_access_key=DO_SECRET_KEY)

    return client

def save_vcf(file_obj):
    client = get_client()

    object_uid = str(uuid.uuid4())
    client.upload_fileobj(file_obj, 'vcf', object_uid)

    return object_uid

def get_vcf(object_uid):
    client = get_client()

    io_obj = io.BytesIO()
    client.download_fileobj('vcf', object_uid, io_obj)
    byte_value = io_obj.getvalue()
    str_value = byte_value.decode()

    return str_value
