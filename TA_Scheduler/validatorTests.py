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

    def test_invalid_email(self):
        self.assertEqual(False, Validator.validate_Email(self, "nathan"))
        self.assertEqual(False, Validator.validate_Email(self, "nathan@yahoo.com"))
        self.assertEqual(False, Validator.validate_Email(self, "!*%#$@gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, " @gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, "nathan.@gmail.com"))
        self.assertEqual(False, Validator.validate_Email(self, " "))
        self.assertEqual(False, Validator.validate_Email(self, "@gmail.com"))