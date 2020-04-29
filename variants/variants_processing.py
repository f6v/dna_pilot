import requests
from django.contrib.auth import get_user_model

from .models import UserVariant, Publication


def create_publication(publication_data, variant):
    Publication.objects.create(
        # variant=variant,
        text=publication_data["title"],
        trait=publication_data["trait"],
        pubmed_id=publication_data["pubmed"],
    )


def fetch_publication(variant):
    response = requests.get(
        "https://myvariant.info/v1/variant/%s" % variant.rsid
    ).json()
    # Response can contain a single object or an array
    if not isinstance(response, list):
        response = [response]
    for response_entry in response:
        if "gwassnps" in response_entry:
            create_publication(response_entry["gwassnps"], variant)


def process_variant(line, user):
    pass
    # variant_line = line.strip()
    # if not variant_line.startswith("#"):
    #     variant_data = variant_line.split('\t')
    #     variant, _ = Variant.objects.get_or_create(
    #         rsid=variant_data[0],
    #         defaults={
    #             'chromosome':variant_data[1],
    #             'position':variant_data[2],
    #         }
    #     )
    #     user_variant = UserVariant.objects.create(
    #         variant=variant,
    #         user=user,
    #         genotype=variant_data[3],
    #     )
    # fetch_publication(variant)


def process_vcf(vcf_content, user_id):
    user = get_user_model().objects.get(id=user_id)
    lines = vcf_content.split("\n")

    for line in lines:
        process_variant(line, user)
