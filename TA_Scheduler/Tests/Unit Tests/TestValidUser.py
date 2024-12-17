import unittest
from TA_Scheduler.models import Validator
from django.test import TestCase



if __name__ == '__main__':
    unittest.main()

class EmailValidatorTests(TestCase):
    def setUp(self):
        pass

    def test_valid_email(self):
        self.assertEqual(True, Validator.validate_Email(self, "nathan@uwm.edu"))
        self.assertEqual(True, Validator.validate_Email(self, "nathan@gmail.com"))
        self.assertEqual(True, Validator.validate_Email(self, "1234nathan@gmail.com"))

    def test_invalid_email(self):
        self.assertEqual(False, Validator.validate_Email(self, "nathan"))
        self.assertEqual(False, Validator.validate_Email(self, "nathan@yahoo.com"))
        self.assertEqual(False, Validator.validate_Email(self, "!*%#$@gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, " @gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, "nathan.@gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, " "))
        self.assertEqual(False, Validator.validate_Email(self, "@gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm@gmail.com"))

    def test_repeated_email(self):
        self.assertEqual(True, Validator.validate_Email(self, "james@gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, "james@gmail.com"))

class PasswordValidatorTests(TestCase):
    def setUp(self):
        pass

    def test_valid_password(self):
        self.assertEqual(True, Validator.validate_Password(self, "1234password!"))

    def test_invalid_password(self):
        self.assertEqual(False, Validator.validate_Password(self, "password"))
        self.assertEqual(False, Validator.validate_Password(self, "password1"))
        self.assertEqual(False, Validator.validate_Password(self, "password!"))
        self.assertEqual(False, Validator.validate_Password(self, "qwertyuiopasdfghjklzxcvbnm1234!"))
        self.assertEqual(False, Validator.validate_Password(self, "h3110 th3re!"))
        self.assertEqual(False, Validator.validate_Password(self, "1a!"))