import pandas as pd
import requests
from io import StringIO
from boto3 import session
from botocore.client import Config
from celery import shared_task
from django.contrib.auth import get_user_model

from .models import Publication, UserVariant
from .object_storage import get_vcf

GWAS_DB_URL = "https://www.ebi.ac.uk/gwas/api/search/downloads/alternative"


@shared_task
def process_vcf(vcf_uid, user_id):
    user = get_user_model().objects.get(pk=user_id)
    vcf_content = get_vcf(vcf_uid)
    vcf_df = pd.read_csv(
        StringIO(vcf_content),
        sep="\t",
        comment="#",
        names=["rsid", "chromosome", "position", "genotype"],
    )
    known_rsids = list(Publication.objects.values_list("rsid", flat=True))
    vcf_df_filtered = vcf_df[vcf_df["rsid"].isin(known_rsids)]
    print("vcf_df_filtered.shape", vcf_df_filtered.shape)
    for _, variant in vcf_df_filtered.iterrows():
        UserVariant.objects.create(
            user=user,
            rsid=variant["rsid"],
            chromosome=variant["chromosome"],
            position=variant["position"],
            genotype=variant["genotype"],
        )


@shared_task
def fetch_publications():
    resp = requests.get(GWAS_DB_URL)
    gwas_df = pd.read_csv(StringIO(resp.text), sep="\t")
    for _, row in gwas_df.iterrows():
        Publication.objects.create(
            rsid=row["SNPS"],
            title=row["STUDY"],
            trait=row["DISEASE/TRAIT"],
            pubmed_id=row["PUBMEDID"],
        )
