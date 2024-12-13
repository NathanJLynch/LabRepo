import unittest
from TA_Scheduler.models import Validator
from django.test import TestCase



if __name__ == '__main__':
    unittest.main()

class HelperTests(TestCase):
    def setUp(self):
        pass

    def test_contains_special(self):
        self.assertEqual(True, Validator.contains_Special(self, "hello!"))
        self.assertEqual(False, Validator.contains_Special(self, "hello"))
        self.assertEqual(True, Validator.contains_Special(self, "!  hello"))

    def test_containts_number(self):
        self.assertEqual(True, Validator.contains_Number(self, "12asdf"))
        self.assertEqual(False, Validator.contains_Number(self, "asdf"))
        self.assertEqual(True, Validator.contains_Number(self, "123 asdf"))

    def test_contains_letter(self):
        self.assertEqual(True, Validator.contains_Letter(self, "hello"))
        self.assertEqual(False, Validator.contains_Letter(self, "1234565"))
        self.assertEqual(True, Validator.contains_Letter(self, "as  df"))

class EmailValidatorTests(TestCase):
    def setUp(self):
        pass

    def test_valid_email(self):
        email_list = ["james@gmail.com", "chris@uwm.edu"]
        self.assertEqual(True, Validator.validate_Email(self, "nathan@uwm.edu", email_list))
        self.assertEqual(True, Validator.validate_Email(self, "nathan@gmail.com", email_list))
        self.assertEqual(True, Validator.validate_Email(self, "1234nathan@gmail.com", email_list))

    def test_invalid_email(self):
        email_list = ["james@gmail.com", "chris@uwm.edu"]
        self.assertEqual(False, Validator.validate_Email(self, "nathan", email_list))
        self.assertEqual(False, Validator.validate_Email(self, "nathan@yahoo.com", email_list))
        self.assertEqual(False, Validator.validate_Email(self, "!*%#$@gmail.com", email_list))
        self.assertEqual(False, Validator.validate_Email(self, " @gmail.com", email_list))
        self.assertEqual(False, Validator.validate_Email(self, "nathan.@gmail.com", email_list))
        self.assertEqual(False, Validator.validate_Email(self, " ", email_list))
        self.assertEqual(False, Validator.validate_Email(self, "@gmail.com", email_list))
        self.assertEqual(False, Validator.validate_Email(self, "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm@gmail.com", email_list))

    def test_repeated_email(self):
        email_list = ["james@gmail.com", "chris@uwm.edu"]
        self.assertEqual(False, Validator.validate_Email(self, "james@gmail.com", email_list))
        self.assertEqual(False, Validator.validate_Email(self, "chris@uwm.edu", email_list))

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

class PhoneValidatorTests(TestCase):
    def setUp(self):
        pass

    def test_valid_phone(self):
        phone_list = ["9204192382", "1234567890"]

        self.assertEqual(True, Validator.validate_phone(self, "0987654321", phone_list))

    def test_invalid_phone(self):
        phone_list = ["9204192382", "1234567890"]
        self.assertEqual(False, Validator.validate_phone(self, "123456789", phone_list))
        self.assertEqual(False, Validator.validate_phone(self, "&123456789", phone_list))
        self.assertEqual(False, Validator.validate_phone(self, "a123456789", phone_list))

    def test_repeated_phone(self):
        phone_list = ["9204192382", "1234567890"]
        self.assertEqual(False, Validator.validate_phone(self, "9204192382", phone_list))