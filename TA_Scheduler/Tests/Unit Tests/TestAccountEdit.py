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
        User.objects.create(full_name=self.full_name, email='email_with_no_at', password=self.password,
                            role_id=self.role)

    def test_correctly_edit_name(self):
        self.user.editusername(self.username, 'Kiari')
        self.assertFalse(self.username == 'Connell')

    def test_correctly_edit_password(self):
        self.user.edit_password(self.username, self.password, 'Bye!')
        self.assertFalse(self.password == 'Hello!')

    def test_correctly_edit_email(self):
        self.user.edit_email(self.username, self.email, 'bye@uwm.edu')
        self.assertFalse(self.email == 'hi@uwm.edu')

    def test_correctly_edit_role(self):
        self.user.edit_role(self.username, 'instructor')
        self.assertFalse(self.role == 'admin')


# test if there's no user
class TestNoUser(TestCase):
    def test_no_such_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(full_name="John Doe")


# Test if there's invalid data inputted
class TestEditInvalidData(TestCase):
    def setUp(self):
        self.full_name = 'John Doe'
        self.password = 'Hello!123'
        self.email = 'hi@uwm.edu'
        self.role = 'admin'
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)

    def test_invalid_username(self):
        result = User.objects.get(id="John Doe")
        # self.user.editusername(self.username, 'h')
        # self.assertTrue(self.user.check_username(self.username), False)

    def test_invalid_password_01(self):
        self.user.edit_password(self.username, self.password, 'hello')
        self.assertTrue(self.user.check_password(self.password), False)

    def test_invalid_password_02(self):
        self.user.edit_password(self.username, self.password, 'h')
        self.assertTrue(self.user.check_password(self.password), False)

    def test_invalid_password_03(self):
        self.user.edit_password(self.username, self.password, '1234')
        self.assertTrue(self.user.check_password(self.password), False)

    def test_invalid_password_04(self):
        self.user.edit_password(self.username, self.password, 'HHHH')
        self.assertTrue(self.user.check_password(self.password), False)

    def test_invalid_email(self):
        self.user.edit_email(self.username, self.email, 'no')
        self.assertTrue(self.user.check_email(self.email), False)