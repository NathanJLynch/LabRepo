from itertools import filterfalse

from django.test import TestCase
from TA_Scheduler.models import Course, User

# Create your tests here

# User Management Tests
class TestAccountCreation(TestCase):

    def setUp(self):
        self.full_name = 'Nathan'
        self.email = 'nathan@uwm.edu'
        self.password = 'Qwerty12345'
        self.role = 'admin'

    def test_create_account(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        self.assertEqual(User.objects.count(), 1)
        # side effect : email sent

    def test_create_account_dup_user(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        User.objects.create(full_name=self.full_name, email='different@uwm.edu', password=self.password, role_id=self.role)
        self.assertFalse(User.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)

    def test_create_account_dup_email(self):
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password, role_id=self.role)
        User.objects.create(full_name="John Doe", email=self.email, password=self.password, role_id=self.role)
        self.assertFalse(User.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)

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


# Account Deletion Tests
class TestAccountDeletion(TestCase):
    def setUp(self):
        self.username = 'Nathan'

    def test_delete_account(self):
        result = self.user.deleteAccount(self.username)
        assert result.success == True
        # side effect : email sent

    def test_delete_nonexistent_user(self):
        self.user.deleteAccount(self.username)
        result = self.user.deleteAccount(self.username)
        assert result.success == False, "user Does Not exist/ Already has been deleted"
        assert result.error("Expected validation to fail for non existent user , but it passed.")

    def test_delete_invalid_course_input(self):
        result = self.user.deleteAccount(self.username)
        assert result.success == False, "Input is not valid"
        assert result.error("Expected validation to fail for invalid user input , but it passed.")

    def test_delete_null_course_input(self):
        result = self.user.deleteAccount(self.username)
        assert result.success == False, "Input is null"
        assert result.error("Expected validation to fail for null user input , but it passed.")


# Course Creation Tests
class TestCourseValidation(TestCase):

    def setup_method(self):
        # Reusable data for tests
        self.courseId = 'CS101'
        self.teacher = 'Micheal Long'
        self.ta = 'Jeffery Thomas'

    def test_login_success(self):
        # Test successful login with valid credentials
        result = self.user.createCourse(self.courseId, self.teacher, self.ta)
        assert result.success == True


    def test_duplicate_course_id(self):
        self.user.createCourse(self.courseId, self.teacher, self.ta)
        result = self.user.createCourse(self.courseId, self.teacher, self.ta)
        # Assert validation fails for duplicate CourseID
        assert result.success == False
        assert result.error ("Expected validation to fail for invalid teacher assignment, but it passed.")

    def test_invalid_teacher_assignment(self):
        result = self.user.createCourse(self.courseId, "M", self.ta)
        # Assert validation fails for invalid teacher assignment
        assert result.success == False
        assert result.error("Expected validation to fail for invalid teacher assignment, but it passed.")

    def test_invalid_ta_assignment(self):
        result = self.user.createCourse(self.courseId, self.teacher, "u")
        # Assert validation fails for invalid TA assignment
        assert result.success == False
        assert result.error("Expected validation to fail for invalid ta assignment, but it passed.")

    def test_missing_course_id(self):
        result = self.user.createCourse("et", self.teacher, self.ta)
        # Assert validation fails for missing CourseID
        assert result.success == False
        assert result.error("Expected validation to fail for invalid teacher assignment, but it passed.")


# Course Deletion Tests
class TestCourseDeletion(TestCase):
    def setup_method(self):
        # Reusable data for tests
        self.courseId = 'CS101'

    def test_delete_success(self):
        # Test successful login with valid credentials
        result = self.user.deleteCourse(self.courseId)
        assert result.success == True

    def test_delete_nonexistent_course(self):
        self.user.deleteCourse(self.courseId)
        result = self.user.deleteCourse(self.courseId)
        assert result.success == False, "Course Does Not exist/ Already has been deleted"
        assert result.error("Expected validation to fail for non existent course , but it passed.")

    def test_delete_invalid_course_input(self):
        result = self.user.deleteCourse("e")
        assert result.success == False, "Input is not valid"
        assert result.error("Expected validation to fail for invalid course input , but it passed.")

    def test_delete_null_course_input(self):
        result = self.user.deleteCourse(" ")
        assert result.success == False, "Course Input is null"
        assert result.error("Expected validation to fail for null course input , but it passed.")

