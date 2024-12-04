from django.contrib.messages import success
from django.db import models
import smtplib


# Create your models here.
## Some Notes: ##
# - I created this based off of the drawn model.
# - List Classes will store the data.
# - Do NOT use models.ManytoMany
# - This is still in testing
# - SectionList Class may not be needed
## End Notes ##

USERNAME_MAX_LENGTH = 20
USERNAME_MIN_LENGTH = 3
PASSWORD_MAX_LENGTH = 32
PASSWORD_MIN_LENGTH = 8
EMAIL_MAX_LENGTH = 72 #64 for before @uwm.edu
special_characters = "!@#$%^&*()-+?_=,<>/"

class Section(models.Model):
    # (-2 for initialization)
    section_id = models.IntegerField(primary_key=True) #section number going from 0, each course will start from 0
    section_type = models.CharField(max_length=7) #specification of section

    def __init__(self, section_id, section_type):
        self.section_id = section_id
        self.section_type = section_type

    def __str__(self):
        string = "[({}){}]".format(self.section_id, self.section_type)
        return string

    def change_SectionType(self, section_type):
        self.section_type = section_type
        self.save()
        return True

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)# course id
    course_name = models.CharField(max_length=15) # name of the course
    section_list = models.IntegerField() # list of sections in the course

    def __init__(self, course_id, course_name, section_list):
        self.course_id = course_id
        self.course_name = course_name
        self.section_list = section_list

    def get_section_type(self, section_id):
        return self.section_list[section_id].section_type

    def __str__(self):
        string = "({}; Sections: ".format(self.course_name)
        #iterates through section list and appends section type onto string
        i = 0
        for section in self.section_list:
            if i > 0:
                string += ", "
            string += "{}".format(section)
            i += 1
        return string

    def add_Section(self, section):
        self.section_list.append(section)
        self.save()
        return True

    def remove_Section(self, section):
        self.section_list.remove(section)
        self.save()
        return True

    def change_CourseName(self, course_name):
        self.course_name = course_name
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
        self.user_id = user_id
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
class SectionList(models.Model):
    section_list = []

    def add_Section(self, section):
        self.section_list.append(section)
        self.save()
        return True

    def remove_Section(self, section):
        self.section_list.remove(section)
        self.save()
        return True

class CourseList(models.Model):
    course_list = []
    TestS = Section(0, "Lecture")
    TestC = Course(0, "CS361", [TestS])
    print(TestC)


    def add_Course(self, course):
        self.course_list.append(course)
        self.save()
        return True

    def remove_Course(self, course):
        self.course_list.remove(course)
        self.save()
        return True

    def get_CourseName(self, course_id):
        return self.course_list[course_id]

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

#--------------------------------------------------------
# User Management
#createAccount method. Unsure if to put in User class or not or to create UserManagement class
class UserManagement(models.Model):
    def createAccount(self, accountdetails):

        username = accountdetails['username']
        email = accountdetails['email']
        password = accountdetails['password']
        role = accountdetails['role']
        first_name = accountdetails['first_name']
        last_name = accountdetails['last_name']
        phone = accountdetails['phone_number']

        if not checkX(self, "username", username):
            return False
            # username requirements: cannot match an active username & must be between 3 and 20 chars & no special chars
        if not checkX(self, "email", email):
            return False
            # email requirements: must contain "@uwm.edu" and must be shorter than 73 chars
        if not checkX(self, "password", password):
            return False
            # password requirements: must contain a special char and a number, must be between 8-32 chars
        if not checkX(self, "role", role):
            return False

        new_user = User(username, first_name, last_name, email, password, role, phone)

        if not UserList.add_User(self, new_user):
            return False

        # still have to send email

        FROM = "TA_SCHEDULER"

        TO = email

        SUBJECT = "Welcome"

        TEXT = "Welcome " + username + " to TA Scheduler"

        if not self.send_email(FROM, TO, SUBJECT, TEXT):
            return False


        new_user.toggle_active()

        return True

    # ----------------------------------------------------

    def send_email(self, FROM, TO, SUBJECT, TEXT):
        return True

    # ----------------------------------------------------

    def editAccountInfo(self, user, updatedinfo):

        if not user in UserList.user_list or updatedinfo is None:
            return False

        if user.email != updatedinfo['email']:
            user.change_email(updatedinfo['email'])

        if user.phone_number != updatedinfo['phone_number']:
            user.change_phone_number(updatedinfo['phone_number'])

        if user.first_name != updatedinfo['first_name']:
            user.change_name(updatedinfo['first_name'], user.last_name)

        if user.last_name != updatedinfo['last_name']:
            user.change_name(user.first_name, updatedinfo['last_name'])

        if user.role_id != updatedinfo['role']:
            user.change_role(updatedinfo['role'])

        if user.password != updatedinfo['password']:
            user.change_password(updatedinfo['password'])

        # send email detailing edits to user email

        return True


#-----------------------------------------------------

def validateRole(self, user, reqrole):
    if user not in UserList.user_list:
        return False

    return user.role_id == reqrole

def checkPermission(self, user, action, resourcetype, resourceid): #incomplete
    ACTIONS = ["create", "read", "update", "delete"]
    RESOURCETYPES = ["user", "course", "lab_section", "notification"]

    # log access attempt for user

    if user not in UserList.user_list or action not in ACTIONS or resourcetype not in RESOURCETYPES:
        return False

    if user.role_id == "TA":
        if resourcetype == "user":
            return (resourceid == user.user_id)

        if resourcetype == "course":

        if resourcetype == "lab_section":
            pass
        if resourcetype == "notification":
            pass

    if user.role_id == "Teacher":

    if user.role_id == "Admin":

    if user.role_id == "Supervisor":


def checkX(type, new):
    TYPES = ["username", "password", "email", "role"]

    if type not in TYPES:
        return False

    if type == "username":
        if new is None or (any(c in special_characters for c in new)) or (
                len(new) < USERNAME_MIN_LENGTH) or (len(new) > USERNAME_MAX_LENGTH):
            return False
        else:
            for i in UserList.user_list:
                if i.username == new:
                    return False
        return True

    if type == "password":
        if (new is None) or (not any(c in special_characters for c in new)) or (
                not any(c.isdigit() for c in new) or len(new) < USERNAME_MIN_LENGTH) or (
                len(new) > USERNAME_MAX_LENGTH) or (len(new) < PASSWORD_MIN_LENGTH):
            return False
        return True

    if type == "email":
        if new is None or "uwm.edu" not in new or len(new) > EMAIL_MAX_LENGTH:
            return False
        else:
            for i in UserList.user_list:
                if i.email == new:
                    return False
        return True

    if type == "role":
        if new is None or new not in RolesList.role_list:
            return False
        return True







