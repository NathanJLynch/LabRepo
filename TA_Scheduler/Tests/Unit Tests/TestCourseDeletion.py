from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from TA_Scheduler.models import Course
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

