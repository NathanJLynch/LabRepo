from django.db import models

# Create your models here.
## Some Notes: ##
# - I created this based off of the drawn model
# - This is made mostly so we have structure and a visual of what we want (It may not be permanent)
# - List Classes may not be needed
# - Unsure if self.save() is needed
## End Notes ##

class Section(models.Model):
    # (-2 for initialization)
    section_id = models.IntegerField(primary_key=True) #section number going from 0, each course will start from 0
    #course_id will get course identity from CourseList
    course_id = models.IntegerField(primary_key=False) #associated with specific course
    section_type = models.IntegerField(primary_key=True)# 0 for lecture, 1 for lab

    def __init__(self, section_id, course_id, section_type):
        self.section_id = section_id
        self.course_id = course_id
        self.section_type = section_type
        self.save()

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=15)
    section_list = models.ManyToManyField(Section)# used for multiple sections

    def __init__(self, course_id, course_name, section_list):
        self.course_id = course_id
        self.course_name = course_name
        self.section_list = section_list
        self.save()

    def add_Section(self, section):
        self.section_list.append(section)
        self.save()
        return True

class CourseList(models.Model):
    course_list = models.ManyToManyField(Course)

    def __init__(self):
        self.course_list = []
        self.save()

    def add_Course(self, course):
        self.course_list.append(course)
        self.save()
        return True

class Role(models.Model):
    role_id = models.IntegerField(primary_key=True)# 0 for Admin, 1 for Supervisor, 2 for Teacher, 3 for TA
    role_name = models.CharField(max_length=15)
    action_access = models.ManyToManyField(int)# each function will have an assigned number

    def __init__(self, role_id, role_name, action_access):
        self.role_id = role_id
        self.role_name = role_name
        self.action_access = action_access
        self.save()

class RoleList(models.Model):
    role_list = models.ManyToManyField(Role)

    def __init__(self):
        self.role_list = []
        self.save()

    def add_Role(self, role):
        self.role_list.append(role)
        self.save()
        return True

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=13)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
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
        self.save()

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

    def toggle_active(self):
        self.is_active = not self.is_active
        self.save()
        return self.is_active
    
class UserList(models.Model):
    user_list = models.ManyToManyField(User)
    def __init__(self):
        self.user_list = []
        self.save()
        
    def add_User(self, user):
        self.user_list.append(user)
        self.save()
        return True
