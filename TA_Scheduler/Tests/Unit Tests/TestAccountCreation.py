import unittest
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase
from TA_Scheduler.models import Course, User

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


class TestAccountCreation(TestCase):

    def setUp(self):
        self.full_name = 'Nathan'
        self.email = 'nathan@uwm.edu'
        self.password = 'Qwerty12345'
        self.role = 'admin'
    def tearDown(self):
        User.objects.get(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role).delete()

    def test_create_account(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        self.assertEqual(User.objects.count(), 1)
        # side effect : email sent

    def test_create_account_dup_user(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        with self.assertRaises(IntegrityError):
            User.objects.create(full_name=self.full_name, email="hi@uwm.edu", password=self.password, role_id=self.role)

    def test_create_account_dup_email(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        User.objects.create(full_name="John Doe", email=self.email, password=self.password, role_id=self.role)
        self.assertFalse(User.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)

    def test_create_account_invalid_details(self):
        User.objects.create(full_name=self.full_name, email='email_with_no_at', password=self.password,
                            role_id=self.role)
        self.assertFalse(User.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)


if __name__ == '__main__':
    unittest.main()
