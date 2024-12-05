from django.db import models

# Create your models here.
## Some Notes: ##
# - I created this based off of the drawn model.
# - List Classes will store the data.
# - Do NOT use models.ManytoMany
# - This is still in testing
# - SectionList Class may not be needed
## End Notes ##

# class Section(models.Model):
#     # (-2 for initialization)
#     section_id = models.IntegerField(primary_key=True) #section number going from 0, each course will start from 0
#     section_type = models.CharField(max_length=7) #specification of section
#
#     def __init__(self, section_id, section_type):
#         self.section_id = section_id
#         self.section_type = section_type
#
#     def __str__(self):
#         string = "[({}){}]".format(self.section_id, self.section_type)
#         return string
#
#     def change_SectionType(self, section_type):
#         self.section_type = section_type
#         self.save()
#         return True

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=50) # name of the course
    course_code = models.CharField(max_length=15, unique = True,null = True)  # course code
    course_sem = models.CharField(max_length=20, unique=True,null= True)  # course sem
    course_instructor = models.CharField(max_length=50, unique=True,null = True)  # course teacher

    def __str__(self):
        return self.course_name


    def change_CourseName(self, course_name, course_code,course_sem, course_instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.course_sem = course_sem
        self.course_instructor = course_instructor
        self.save()
        return True

class Role(models.Model):
    #role_id = models.IntegerField(primary_key=True)# 0 for Admin, 1 for Supervisor, 2 for Teacher, 3 for TA
    role_name = models.CharField(max_length=15)
    action_access = models.IntegerField()# each function will have an assigned number

    def __init__(self, role_id, role_name, action_access):
        self.role_id = role_id
        self.role_name = role_name
        self.action_access = action_access

    def __str__(self):
        return self.role_name


class User(models.Model):
    #user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=13)
    role_id = models.IntegerField()
    is_active = models.BooleanField(default=False)# not sure how this will work yet

    def __init__(self, user_id, first_name, last_name, email, password, phone_number, role_id):
        #self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.role_id = role_id
        self.is_active = False

    def change_email(self, new_email):
        self.email = new_email
        self.save()
        return True

    def change_password(self, new_password):
        self.password = new_password
        self.save()
        return True

    def change_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number
        self.save()
        return True

    def change_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.save()
        return True

    def change_role(self, role_id):
        self.role_id = role_id
        self.save()
        return True

    def toggle_active(self):
        self.is_active = not self.is_active
        self.save()
        return self.is_active



# Data Structure Classes
# class SectionList(models.Model):
#     section_list = []
#
#     def add_Section(self, section):
#         self.section_list.append(section)
#         self.save()
#         return True
#
#     def remove_Section(self, section):
#         self.section_list.remove(section)
#         self.save()
#         return True
#
# class CourseList(models.Model):
#     course_list = []
#     TestS = Section(0, "Lecture")
#     TestC = Course(0, "CS361", [TestS])
#     print(TestC)
#
#
#     def add_Course(self, course):
#         self.course_list.append(course)
#         self.save()
#         return True
#
#     def remove_Course(self, course):
#         self.course_list.remove(course)
#         self.save()
#         return True
#
#     def get_CourseName(self, course_id):
#         return self.course_list[course_id]

class RolesList(models.Model):
    role_list = []

    TA = Role(0, "TA", [0])
    Teacher = Role(1, "Teacher", [1,0])
    Admin = Role(2, "Admin", [-1])# -1 means all access for simplicity
    Supervisor = Role(3, "Supervisor", [3,2,1,0])
    role_list.append(TA)
    role_list.append(Teacher)
    role_list.append(Admin)
    role_list.append(Supervisor)
    print(role_list)

    def get_RoleName(self, role_id):
        return self.role_list[role_id].role_name

class UserList(models.Model):
    user_list = []
    #Test = User(0, "John", "Doe", "address@uwm.edu", "Password123!", "4444444444", RolesList.role_list[0])

    def add_User(self, user):
        self.user_list.append(user)
        self.save()
        return True

    def remove_User(self, user):
        self.user_list.remove(user)
        self.save()
        return True



