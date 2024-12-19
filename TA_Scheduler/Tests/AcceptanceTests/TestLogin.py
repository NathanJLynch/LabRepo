from django.test import TestCase
from django.urls import reverse

from TA_Scheduler.models import User

class LoginTests(TestCase):
    def setUp(self):
        self.full_name = "John Doe"
        self.email = "jdoe@uwm.edu"
        self.password = "Password123!"
        self.role = "admin"
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
    def test_successful_login(self):
        response = self.client.post(reverse("LoginPage"), {"full_name": self.full_name, "password" : self.password})
        self.assertRedirects(response, reverse("homePage"))
    def test_wrong_full_name(self):
        response = self.client.post(reverse("LoginPage"), {"full_name": "brian", "password": self.password}, follow = True)
        self.assertRedirects(response, reverse("LoginPage"))
        messages = response.context.get('messages', [])
        self.assertEqual(len(messages), 1)
    def test_wrong_password(self):
        response = self.client.post(reverse("LoginPage"), {"full_name": self.full_name, "password": "wrong"},
                                    follow=True)
        self.assertRedirects(response, reverse("LoginPage"))
        messages = response.context.get('messages', [])
        self.assertEqual(len(messages), 1)

