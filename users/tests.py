from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="user@test.com", password="testpass123")
        self.assertEqual(user.email, "user@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("admin@test.com", "admin")
        self.assertEqual(admin_user.email, "admin@test.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@test.com", password="foo", is_superuser=False
            )


class SignupTests(TestCase):
    def setUp(self):
        self.url = reverse("account_signup")

    def test_signup_template(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")
        self.assertContains(response, "Sign Up")

    def test_signup_request(self):
        user_data = {
            "email": "new_user@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        response = self.client.post(self.url, user_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(
            get_user_model().objects.all()[0].email, "new_user@example.com"
        )
