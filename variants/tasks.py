from boto3 import session
from botocore.client import Config
from celery import shared_task

from .variants_processing import process_vcf
from .object_storage import get_vcf


@shared_task
def process_file(vcf_uid, user_id):
    object_content = get_vcf(vcf_uid)
    process_vcf(object_content, user_id)
