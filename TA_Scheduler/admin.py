from django.contrib import admin

from TA_Scheduler.models import UserList, Course, CourseList, RolesList, User, Role

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(RolesList)
admin.site.register(UserList)
admin.site.register(CourseList)
admin.site.register(Role)