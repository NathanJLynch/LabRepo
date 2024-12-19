import unittest
from django.test import TestCase
from django.urls import reverse
from TA_Scheduler.models import User

class create_account(TestCase):
    def setUp(self):
        pass
    def create_account_success(self):
        pass
    def invalid_email(self):
        pass
    def passwords_dont_match(self):
        pass
    def incorrect_phone_number(self):
        pass
class edit_account(TestCase):
    def setUp(self):
        pass
    def successful_name_change(self):
        pass
    def successful_email_change(self):
        pass
    def successful_password_change(self):
        pass
    def successful_phone_number_change(self):
        pass
    def successful_role_change(self):
        pass
    def permission_denied_role(self):
        pass
    def name_taken(self):
        pass
    