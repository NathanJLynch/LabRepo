from django.test import TestCase

from django.urls import reverse

from TA_Scheduler.models import Course

import datetime


class CourseTestCase(TestCase):
    def setUp(self):
        self.course_id = 1
        self.course_name = "Software Stuff"
        self.course_code = "CS635"
        self.semester = "Fall 2025"
        self.course_instructor = "Jesse Blanche"
        self.start_time = datetime.time(9,30)
        self.end_time = datetime.time(10,20)
        self.days = "M, W"
        self.date = datetime.date(2024,9,5)

    def test_CourseCreationSuccess(self):
        print("Test Course Successfully Created:")
        response = self.client.post(reverse("CreateCourse"), {
            "course_name":self.course_name,
            "course_code":self.course_code,
            "course_sem":self.semester,
            "course_instructor":self.course_instructor,
            "course_id":self.course_id,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "days":self.days,
            "date":self.date,})
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
            "course_instructor":self.course_instructor,
            "course_id": self.course_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "days": self.days,
            "date": self.date,
        })
        print("\tStatus:",response.status_code)
        objectsFound = Course.objects.count()
        print("\tObjects:",objectsFound)
        self.assertEqual (objectsFound, 0, "An Object was Created") #This means no object was created
        print("\tResult: Passed!")

        #Part 2
        print("Missing Object Test:")
        response = self.client.post(reverse("CreateCourse"), {
            "course_name":self.course_name,
            "course_code":self.course_code,
            #"course_sem": self.semester,  # Missing Object
            "course_instructor":self.course_instructor,
            "course_id": self.course_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "days": self.days,
            "date": self.date,
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
            "course_sem": self.semester,
            "course_instructor":self.course_instructor,
            "course_id": self.course_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "days": self.days,
            "date": self.date,
        })
        print("\tStatus:",response.status_code)
        objectsFound = Course.objects.count()
        print("\tObjects:",objectsFound)

        print("\tDeleting Course...")
        course = Course.objects.get(course_code=self.course_code)
        course.delete()
        print("\tStatus:",response.status_code)
        objectsFound = Course.objects.count()
        print("\tObjects:",objectsFound)

        self.assertEqual (objectsFound, 0, "Object Not Deleted")
        print("\tResult: Passed!")

    def test_CourseNameChange(self):
        print("Test Course Name Change:")
        response = self.client.post(reverse("CreateCourse"), {
            "course_name":self.course_name,
            "course_code":self.course_code,
            "course_sem": self.semester,
            "course_instructor":self.course_instructor,
            "course_id": self.course_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "days": self.days,
            "date": self.date,
        })
        course = Course.objects.get(course_code=self.course_code)
        print("\tPrevious Course Name:",course.course_name)
        print("\tChanging Course Name...")
        course.course_name = "Brand New Software"
        print("\tNew Course Name:",course.course_name)

        self.assertNotEqual(self.course_name, course.course_name)
        print("\tResult: Passed!")
