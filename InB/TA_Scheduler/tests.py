from django.test import TestCase

# Create your tests here.

# Account Creation Tests
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
        assert result.success == False, "Input is null"
        assert result.error("Expected validation to fail for null course input , but it passed.")
