from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase
from TA_Scheduler.models import Course, User

class TestEditAccounts(TestCase):
    def setUp(self):
        self.full_name = 'Connell'
        self.password = 'Hello!'
        self.email = 'hi123@uwm.edu'
        self.role = 'admin'
        self.phone = 000000000
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password,
                            role_id=self.role)

    def test_correctly_edit_name(self):
        user = User.objects.get(full_name =self.full_name)
        user.full_name = "dummy name"
        self.assertFalse(user.full_name, self.full_name)

    def test_correctly_edit_password(self):
        user = User.objects.get(full_name=self.full_name)
        user.password = "newPassword"
        self.assertFalse(user.password, self.password)

    def test_correctly_edit_email(self):
        user = User.objects.get(full_name=self.full_name)
        user.email = "newemail@uwm.edu"
        self.assertFalse(user.email, self.email)

    def test_correctly_edit_role(self):
        user = User.objects.get(full_name=self.full_name)
        user.role_id = "instructor"
        self.assertFalse(user.role_id, self.role)
    def test_correctly_edit_phone(self):
        user = User.objects.get(full_name=self.full_name)
        user.phone = 1111111111
        self.assertFalse(user.phone, self.phone)


# test if there's no user
class TestNoUser(TestCase):
    def test_no_such_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(full_name="John Doe")

