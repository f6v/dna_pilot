import os
import responses
import boto3
import uuid
from moto import mock_s3
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files.base import ContentFile
from django.contrib.auth.models import Permission

from .models import UserVariant, Recommendation, Publication
from .tasks import fetch_publications, process_vcf


class VariantsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.client.login(email="user@example.com", password="testpass123")

    def test_upload_page(self):
        response = self.client.get(reverse("variant_upload"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit")

    def test_variant_detail_with_permission(self):
        permission = Permission.objects.get(codename='premium_status')
        self.user.user_permissions.add(permission)

        variant = UserVariant.objects.create(
            user=self.user,
            rsid="rs4477212",
            chromosome="1",
            position="82154",
            genotype="AA",
        )
        recommendation = Recommendation.objects.create(
            rsid="rs4477212", text="Do not eat sugar."
        )
        publication = Publication.objects.create(
            rsid="rs4477212",
            title="Sugar consumption",
            trait="metabolism",
            pubmed_id=123,
        )

        response = self.client.get(variant.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, variant.position)
        self.assertContains(response, recommendation.text)
        self.assertContains(response, publication.title)
        self.assertContains(response, publication.trait)

    def test_variant_detail_without_permission(self):
        variant = UserVariant.objects.create(
            user=self.user,
            rsid="rs4477212",
            chromosome="1",
            position="82154",
            genotype="AA",
        )
        recommendation = Recommendation.objects.create(
            rsid="rs4477212", text="Do not eat sugar."
        )

        response = self.client.get(variant.get_absolute_url())

        self.assertNotContains(response, recommendation.text)

    def test_list_with_no_variants(self):
        response = self.client.get(reverse("variant_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload now")

    def test_list_with_variants(self):
        variant = UserVariant.objects.create(
            user=self.user,
            rsid="rs4477212",
            chromosome="1",
            position="82154",
            genotype="AA",
        )

        response = self.client.get(reverse("variant_list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Upload now")
        self.assertContains(response, variant.position)

    @responses.activate
    def test_fetch_publications(self):
        db_file = open(
            os.path.join(settings.BASE_DIR, "variants/fixtures/gwas_db.tsv"), "rb"
        )

        responses.add(
            responses.GET,
            "https://www.ebi.ac.uk/gwas/api/search/downloads/alternative",
            body=db_file,
            status=200,
        )

        self.assertEqual(Publication.objects.count(), 0)

        fetch_publications.run()

        self.assertEqual(Publication.objects.count(), 19)

    # @mock_s3
    # def test_process_vcf(self):
    #     vcf_file = open(
    #         os.path.join(settings.BASE_DIR, "variants/fixtures/user1.vcf"), "rb"
    #     )
    #     do_spaces = boto3.client("s3", region_name="ams3")
    #     do_spaces.create_bucket(Bucket="vcf")
    #     vcf_uid = str(uuid.uuid4())
    #     do_spaces.put_object(Bucket="vcf", Key=vcf_uid, Body=vcf_file)
    #
    #     Publication.objects.create(
    #         rsid="rs4477212", title="Title", trait="Trait", pubmed_id=123
    #     )
    #
    #     process_vcf.run(vcf_uid, self.user.id)
    #
    #     self.assertEqual(UserVariant.objects.count(), 2)
