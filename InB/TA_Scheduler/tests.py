from itertools import filterfalse

from django.test import TestCase

# Create your tests here.
class TestEditAccounts(TestCase):
    def setUp(self):
        self.username = 'Connell'
        self.password = 'Hello!'
        self.email = 'hi@uwm.edu'
        self.role = 'admin'
        self.user.createaccount(self.username, self.password, self.email, self.role)
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
        self.user.edit_role(self.username, 'intructor')
        self.assertFalse(self.role == 'admin')
class TestNoUser(TestCase):
    def test_no_such_user(self):
        self.user.edit_username('Connor', 'Michael')
        self.assertRaises(ValueError)
class TestInvalidData(TestCase):
    def setUp(self):
        self.username = 'Connell'
        self.password = 'Hello!'
        self.email = 'hi@uwm.edu'
        self.role = 'admin'
    def test_invalid_username(self):
        self.user.editusername(self.username, 'h')
        self.assertTrue(self.user.check_username(self.username), False)
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






