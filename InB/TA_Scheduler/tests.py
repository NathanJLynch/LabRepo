from django.test import TestCase

# Create your tests here.

# User Management Tests
class TestAccountCreation(TestCase):

    def setUp(self):
        self.username = 'Nathan'
        self.email = 'nathan@uwm.edu'
        self.password = 'Qwerty12345'
        self.role = 'Supervisor'

    def test_create_account(self):
        result = self.user.createAccount('Jimbo', 'Jimbo@uwm.edu', self.password, self.role)
        assert result.success == True
        # side effect : email sent

    def test_create_account_dup_user(self):
        self.user.createAccount('Jones', 'Jones@uwm.edu', self.password, self.role)
        result = self.user.createAccount('Jones', 'Connor@uwm.edu', self.password, self.role)
        assert result.success == False, "account with same username already exists"

    def test_create_account_dup_email(self):
        self.user.createAccount('Bimbo', 'Bimbo@uwm.edu', self.password, self.role)
        result = self.user.createAccount('Connor', 'Bimbo@uwm.edu', self.password, self.role)
        assert result.success == False, "account with same email already exists"

    def test_create_account_invalid_details(self):
        result = self.user.createAccount('a', 'emailwithno_at', 'a', 'banana')
        assert result.success == False, "account with invalid details"
        assert result.validation_errors != None

    def welcome_email_test(self):
        self.user.createAccount('Paul', 'Paul@uwm.edu', self.password, self.role)
        result = self.user.emailsent('Paul@uwm.edu')
        assert result.success == True





