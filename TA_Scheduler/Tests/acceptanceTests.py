import unittest
from django.test import TestCase
from django.urls import reverse

from TA_Scheduler.models import Course


class CourseTestCase(TestCase):
    def setUp(self):
        self.course_name = "Software Stuff"
        self.course_code = "CS635"
        self.semester = "Fall 2025"
        self.course_instructor = "Jesse Blanche"

    def test_CourseCreationSuccess(self):
        print("Test Course Successfully Created:")
        response = self.client.post(reverse("CreateCourse"), {
            "course_name":self.course_name,
            "course_code":self.course_code,
            "course_sem":self.semester,
            "course_instructor":self.course_instructor})
        self.assertRedirects(response, "/Courses")
        # response status_code list: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
        print("\tStatus:",response.status_code)# 302 means FOUND/a successful redirect, 200 means OK
        objectsFound = Course.objects.count()
        print("\tObjects:", objectsFound)
        self.assertEqual (objectsFound, 1, "No Object was Created")  # This means an object was created
        print("\tResult: Passed!")

    def test_CourseCreationFailure(self):
        print("Test Course Unsuccessful Creation:")
        #Part 1
        print("Invalid Value Test:")
        response = self.client.post(reverse("CreateCourse"), {
            "course_name":self.course_name,
            "course_code":'', #Invalid Value
            "course_sem": self.semester,
            "course_instructor":self.course_instructor
        })
        print("\tStatus:",response.status_code)
        objectsFound = Course.objects.count()
        print("\tObjects:",objectsFound)
        self.assertEqual (objectsFound, 0, "An Object was Created") #This means no object was created
        print("\tResult: Passed!")

        #Part 2
        print("Missing Value Test:")
        response = self.client.post(reverse("CreateCourse"), {
            "course_name":self.course_name,
            "course_code":self.course_code,
            #"course_sem": self.semester,  # Missing Value
            "course_instructor":self.course_instructor
        })
        print("\tStatus:",response.status_code)
        objectsFound = Course.objects.count()
        print("\tObjects:",objectsFound)
        self.assertEqual (objectsFound, 0, "An Object was Created") #This means no object was created
        print("\tResult: Passed!")

    def test_CourseDeleteCourse(self):
        print("Test Course Delete Course:")
        response = self.client.post(reverse("CreateCourse"), {
            "course_name":self.course_name,
            "course_code":self.course_code,
            "course_sem": self.semester,  # Missing Object
            "course_instructor":self.course_instructor
        })
        print("\tStatus:",response.status_code)
        objectsFound = Course.objects.count()
        print("\tObjects:",objectsFound)

        print("\tDeleting Course...")
        # Insert Code to Delete Object...
        # response = self.client.post(reverse("DeleteCourse"), {}) #No Deletion Page Made!
        print("\tStatus:",response.status_code)
        objectsFound = Course.objects.count()
        print("\tObjects:",objectsFound)

        self.assertEqual (objectsFound, 0, "Object Not Deleted")
        print("\tResult: Passed!")


