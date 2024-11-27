from itertools import filterfalse

from django.test import TestCase

# Create your tests here

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
        
#test for editing accounts
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
        
#test if there's no user
class TestNoUser(TestCase):
    def test_no_such_user(self):
        self.user.edit_username('Connor', 'Michael')
        self.assertRaises(ValueError)
        
#Test if there's invalid data inputted
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


# Course Creation Tests
class TestCourseValidation(TestCase):

    def setup_method(self):
        # Reusable data for tests
        self.valid_course_details = {
            "course_id" : "CS101",
            "teacher": "Micheal Long",
            "ta": "Jeffery Thomas"
        }

        def test_login_success(self):
            # Test successful login with valid credentials
            result = self.user.TestCourseValidation(self.valid_course_details)
            assert result.success == True


        def test_duplicate_course_id(self):
            result = self.user.TestCourseValidation(self.valid_course_details)
            result2 = self.user.TestCourseValidation(self.valid_course_details)
            # Assert validation fails for duplicate CourseID
            assert result2.success == False
            assert result.error ("Expected validation to fail for invalid teacher assignment, but it passed.")

    def test_invalid_teacher_assignment(self):
        # Setup: Create a course with an invalid teacher ID
        self.invalid_course_detailsT = {
            "course_id": "CS101",
            "teacher": "M",
            "ta": "Jeffery Thomas"
        }
        result = self.user.TestCourseValidation(self.invalid_course_detailsT)
        # Assert validation fails for invalid teacher assignment
        assert result.success == False
        assert result.error("Expected validation to fail for invalid teacher assignment, but it passed.")

    def test_invalid_ta_assignment(self):
        # Setup: Create a course with an invalid TA ID
        self.invalid_course_detailsTA = {
            "course_id": "CS101",
            "teacher": "Micheal Long",
            "ta": " J"
        }
        result = self.user.TestCourseValidation(self.invalid_course_detailsTA)

        # Assert validation fails for invalid TA assignment
        assert result.success == False
        assert result.error("Expected validation to fail for invalid teacher assignment, but it passed.")

    def test_missing_course_id(self):
        # Setup: Create a course with a missing CourseID
        self.invalid_course_detailsCI = {
            "course_id": "CS101",
            "teacher": "",
            "ta": "Jeffery Thomas"
        }
        result = self.user.TestCourseValidation(self.invalid_course_detailsCI)

        # Assert validation fails for missing CourseID
        assert result.success == False
        assert result.error("Expected validation to fail for invalid teacher assignment, but it passed.")


# Course Deletion Tests
class TestCourseDeletion(TestCase):
    def setup_method(self):
        # Reusable data for tests
        self.valid_course_details = {
            "course_id": "CS101",
            "teacher": "Micheal Long",
            "ta": "Jeffery Thomas"
        }
