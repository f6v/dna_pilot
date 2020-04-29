from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files.base import ContentFile
import responses

from .models import UserVariant, Recommendation, Publication


class VariantsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.client.login(email="user@example.com", password="testpass123")
        self.vcf_content = (
            b"# rsid	chromosome	position	genotype\n"
            b"rs4477212	1	82154	AA\n"
            b"rs3094315	1	752566	AA\n"
        )
        self.vcf_content_single_snp = (
            b"# rsid	chromosome	position	genotype\n" b"rs4477213	1	82154	AA\n"
        )

    def test_upload_page(self):
        response = self.client.get(reverse("variant_upload"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit")

    @responses.activate
    def test_submit_data(self):
        responses.add(
            responses.GET,
            "https://myvariant.info/v1/variant/rs4477212",
            json={
                "gwassnps": {
                    "pubmed": 21878437,
                    "title": "Title rs4477212",
                    "trait": "Trait rs4477212",
                }
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://myvariant.info/v1/variant/rs3094315",
            json={
                "gwassnps": {
                    "pubmed": 21878438,
                    "title": "Title rs3094315",
                    "trait": "Trait rs3094315",
                }
            },
            status=200,
        )

        file = ContentFile(self.vcf_content, name="my_vcf.txt")

        response = self.client.post(
            reverse("variant_upload"), {"vcf_file": file}, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse("variant_list"))
        self.assertEqual(UserVariant.objects.filter(user=self.user).count(), 2)
        self.assertEqual(Publication.objects.count(), 2)

    @responses.activate
    def test_submit_data_multiple_entries_in_response(self):
        responses.add(
            responses.GET,
            "https://myvariant.info/v1/variant/rs4477213",
            json=[
                {
                    "gwassnps": {
                        "pubmed": 21878440,
                        "title": "Title rs4477212 1",
                        "trait": "Trait rs4477212 1",
                    }
                },
                {
                    "gwassnps": {
                        "pubmed": 21878441,
                        "title": "Title rs4477212 2",
                        "trait": "Trait rs4477212 2",
                    }
                },
            ],
            status=200,
        )

        file = ContentFile(self.vcf_content_single_snp, name="my_vcf.txt")

        response = self.client.post(
            reverse("variant_upload"), {"vcf_file": file}, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Publication.objects.count(), 2)

    def test_variant_detail(self):
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

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, variant.position)
        self.assertContains(response, recommendation.text)

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
