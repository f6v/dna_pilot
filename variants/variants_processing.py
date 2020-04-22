import requests

from .models import Variant, UserVariant, Publication


def create_publication(publication_data, variant):
    Publication.objects.create(
        variant=variant,
        text=publication_data['title'],
        trait=publication_data['trait'],
        pubmed_id=publication_data['pubmed']
    )

def fetch_publication(variant):
    response = requests.get('https://myvariant.info/v1/variant/%s'
                            % variant.rsid).json()
    # Response can contain a single object or an array
    if not isinstance(response, list):
        response = [response]
    for response_entry in response:
        if 'gwassnps' in response_entry:
            create_publication(response_entry['gwassnps'], variant)

def process_variant(line, current_user):
    variant_line = line.decode().strip()
    if not variant_line.startswith("#"):
        variant_data = variant_line.split('\t')
        variant, _ = Variant.objects.get_or_create(
            rsid=variant_data[0],
            defaults={
                'chromosome':variant_data[1],
                'position':variant_data[2],
            }
        )
        user_variant = UserVariant.objects.create(
            variant=variant,
            user=current_user,
            genotype=variant_data[3],
        )
        fetch_publication(variant)

def handle_uploaded_file(file, current_user):
    for line in file:
        process_variant(line, current_user)
