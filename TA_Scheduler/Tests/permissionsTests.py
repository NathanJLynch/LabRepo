import unittest
from TA_Scheduler.models import CheckPermissions, User, Course
from django.test import TestCase

if __name__ == '__main__':
    unittest.main()

class CheckPermissionsTests(TestCase):
    def setUp(self):
        self.course_code = "CS361"
        self.course_sem = "fall-2024"
        self.course_name = "Intro to Software Engineering"
        self.course_instructor = "John Doe"
        User.objects.create(full_name="Nathan Lynch", email="Nathan@uwm.edu", password="Querty12345!", role_id="TA", phone=9204192381)
        User.objects.create(full_name="Paul Jones", email="Paul@uwm.edu", password="Querty12345!", role_id="Supervisor", phone=9204192381)
        User.objects.create(full_name="John Doe", email="John@uwm.edu", password="Querty12345!", role_id="Teacher", phone=9204192381)
        Course.objects.create(course_name=self.course_name, course_code=self.course_code, course_sem=self.course_sem,
                              course_instructor=self.course_instructor)


    def testEditPermissions(self):
        self.assertEqual(True, CheckPermissions.check_edit_user_permissions(self,User.objects.get(self, full_name="Nathan Lynch"),
                        User.objects.get(self, full_name="Nathan Lynch")))
        self.assertEqual(False, CheckPermissions.check_edit_user_permissions(self,User.objects.get(self, full_name="Nathan Lynch"),
                        User.objects.get(self, full_name="Paul Jones") ))
        self.assertEqual(True, CheckPermissions.check_edit_user_permissions(self,User.objects.get(self, full_name="Paul Jones"),
                        User.objects.get(self, full_name="Nathan Lynch") ))

    def testDeleteAndCreatePermissions(self):
        self.assertEqual(True, CheckPermissions.check_create_delete_permissions(self,
                        User.objects.get(self, full_name="Paul Jones")))
        self.assertEqual(False, CheckPermissions.check_create_delete_permissions(self,
                        User.objects.get(self,full_name="Nathan Lynch")))

    def testEditCoursePermissions(self):
        self.assertEqual(True, CheckPermissions.check_edit_course_permissions(self,
            User.objects.get(self, full_name="John Doe"), Course.objects.get(course_name="Intro to Software Engineering")))
        self.assertEqual(False, CheckPermissions.check_edit_course_permissions(self,
            User.objects.get(self,full_name="Nathan Lynch"), Course.objects.get(course_name="Intro to Software Engineering")))
        self.assertEqual(True, CheckPermissions.check_edit_course_permissions(self,
            User.objects.get(self, full_name="Paul Jones"),Course.objects.get(course_name="Intro to Software Engineering")))