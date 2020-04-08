from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Variant


class VariantsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.login(email='user@example.com', password='testpass123')

    def test_with_no_variants(self):
        response = self.client.get(reverse('variants_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload now')

    def test_with_variants(self):
        variant = Variant.objects.create(
            user=self.user,
            rsid='rs4477212',
            chromosome='1',
            position=798959,
            genotype='AA'
        )

        response = self.client.get(reverse('variants_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Upload now')
        self.assertContains(response, variant.rsid)
