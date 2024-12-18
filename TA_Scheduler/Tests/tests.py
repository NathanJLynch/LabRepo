from itertools import filterfalse

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase
from TA_Scheduler.models import Course, User

# Create your tests here

# User Management Tests
class TestAccountCreation(TestCase):

    def setUp(self):
        self.full_name = 'Nathan Lynch'
        self.email = 'nathan@uwm.edu'
        self.password = 'Qwerty12345!'
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
        User.objects.create(full_name=self.full_name, email='email_with_no_at', password=self.password, role_id=self.role)
        self.assertFalse(User.objects.count(), 2)
        self.assertEqual(User.objects.count(), 1)
        
#test for editing accounts
class TestEditAccounts(TestCase):
    def setUp(self):
        self.full_name = 'Connell'
        self.password = 'Hello!'
        self.email = 'hi123@uwm.edu'
        self.role = 'admin'
        User.objects.create(full_name=self.full_name, email='email_with_no_at', password=self.password, role_id=self.role)
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
        
#test if there's no user
class TestNoUser(TestCase):
    def test_no_such_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(full_name="John Doe")
        
#Test if there's invalid data inputted
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


# Account Deletion Tests
class TestAccountDeletion(TestCase):
    def setUp(self):
        self.full_name = 'John Doe'
        self.password = 'Hello!123'
        self.email = 'hi@uwm.edu'
        self.role = 'admin'
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password,
                            role_id=self.role)

    def test_delete_account(self):
        User.objects.get(full_name = self.full_name).delete()
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(full_name= self.full_name)
        # side effect : email sent

    def test_delete_nonexistent_user(self):
        User.objects.get(full_name=self.full_name).delete()
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(full_name=self.full_name).delete()

    # def test_delete_invalid_course_input(self):
    #     result = self.user.deleteAccount(self.username)
    #     assert result.success == False, "Input is not valid"
    #     assert result.error("Expected validation to fail for invalid user input , but it passed.")
    #
    # def test_delete_null_course_input(self):
    #     result = self.user.deleteAccount(self.username)
    #     assert result.success == False, "Input is null"
    #     assert result.error("Expected validation to fail for null user input , but it passed.")


# Course Creation Tests
class TestCourseValidation(TestCase):

    def setUp(self):
        # Reusable data for tests
        self.course_code = "CS361"
        self.course_sem = "fall-2024"
        self.course_name = "Intro to Software Engineering"
        self.course_instructor = "Jayson Rock"

    def test_successful_course_creation(self):
        # Test successful login with valid credentials
        Course.objects.create(course_name=self.course_name, course_code=self.course_code, course_sem=self.course_sem,
                              course_instructor=self.course_instructor)
        self.assertEqual(Course.objects.count(), 1)


    def test_duplicate_course_id(self):
        Course.objects.create(course_name=self.course_name, course_code=self.course_code, course_sem=self.course_sem,
                              course_instructor=self.course_instructor)
        with self.assertRaises(IntegrityError):
            Course.objects.create(course_name=self.course_name, course_code=self.course_code,
                                  course_sem=self.course_sem,
                                  course_instructor=self.course_instructor)

    # def test_invalid_teacher_assignment(self):
    #     result = self.user.createCourse(self.courseId, "M", self.ta)
    #     # Assert validation fails for invalid teacher assignment
    #     assert result.success == False
    #     assert result.error("Expected validation to fail for invalid teacher assignment, but it passed.")

    # def test_invalid_ta_assignment(self):
    #     result = self.user.createCourse(self.courseId, self.teacher, "u")
    #     # Assert validation fails for invalid TA assignment
    #     assert result.success == False
    #     assert result.error("Expected validation to fail for invalid ta assignment, but it passed.")
    #
    # def test_missing_course_id(self):
    #     result = self.user.createCourse("et", self.teacher, self.ta)
    #     # Assert validation fails for missing CourseID
    #     assert result.success == False
    #     assert result.error("Expected validation to fail for invalid teacher assignment, but it passed.")


# Course Deletion Tests
class TestCourseDeletion(TestCase):
    def setUp(self):
        # Reusable data for tests
        self.course_code = "CS361"
        self.course_sem = "fall-2024"
        self.course_name = "Intro to Software Engineering"
        self.course_instructor = "Jayson Rock"
        Course.objects.create(course_name=self.course_name, course_code=self.course_code, course_sem=self.course_sem,
                              course_instructor=self.course_instructor)


    def test_delete_success(self):
        # Test successful login with valid credentials
        Course.objects.get(course_name=self.course_name).delete()
        self.assertEqual(Course.objects.count(), 0)

    def test_delete_nonexistent_course(self):
        self.assertEqual(Course.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(course_name="intro to blah studies").delete()

