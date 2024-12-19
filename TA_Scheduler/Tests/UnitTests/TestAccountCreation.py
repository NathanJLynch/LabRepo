import unittest
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase
from TA_Scheduler.models import Course, User


class TestAccountCreation(TestCase):

    def setUp(self):
        self.full_name = 'Nathan'
        self.email = 'nathan@uwm.edu'
        self.password = 'Qwerty12345'
        self.role = 'admin'
        self.phone = 0000000000
    def test_create_account(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password,phone = self.phone, role_id=self.role)
        self.assertEqual(User.objects.count(), 1)
        # side effect : email sent

    def test_create_account_dup_user(self):
        print("line 22")
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        print("line 24")
        with self.assertRaises(IntegrityError):
            User.objects.create(full_name=self.full_name, email="hi@uwm.edu", password=self.password, role_id=self.role)
    def test_create_account_dup_email(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        with self.assertRaises(IntegrityError):
            User.objects.create(full_name="John Doe", email=self.email, password=self.password, role_id=self.role)


if __name__ == '__main__':
    unittest.main()
