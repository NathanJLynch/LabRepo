import unittest
from django.test import TestCase
from django.urls import reverse
from TA_Scheduler.models import User

class TestHomeScreen(TestCase):

    def setUp(self):
        self.full_name = "John Doe"
        self.email = "jdoe@uwm.edu"
        self.password = "Password123!"
        self.role = "admin"
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
    def test_go_to_view_accounts(self):
        response = self.client.get('/ListAccounts')
        self.assertEqual(response.status_code, 200)
    def test_go_to_edit_account(self):
        response = self.client.get('/EditAccount')
        self.assertEqual(response.status_code, 200)
    def test_go_to_create_account(self):
        response = self.client.get('/CreateAccount')
        self.assertEqual(response.status_code, 200)
    def test_go_to_view_courses(self):
        response = self.client.get('/Courses')
        self.assertEqual(response.status_code, 200)
    def test_go_to_notifications(self):
        response = self.client.get('/Notifications')
        self.assertEqual(response.status_code, 200)
    def test_logout(self):
        response = self.client.get('/LoginPage')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
