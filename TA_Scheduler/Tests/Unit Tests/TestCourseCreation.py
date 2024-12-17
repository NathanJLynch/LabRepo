from django.db import IntegrityError
from django.test import TestCase
from TA_Scheduler.models import Course


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
