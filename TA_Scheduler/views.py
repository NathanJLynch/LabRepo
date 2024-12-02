from django.shortcuts import render
from django.views.generic import TemplateView

class LoginPageView(TemplateView):
    template_name = 'LoginPage.html'


class HomePageView(TemplateView):
    template_name = 'homePage.html'


class coursesPageView(TemplateView):
    template_name = 'courses.html'

class CreateAccountPageView(TemplateView):
    template_name = 'create-account.html'

class EditAccountPageView(TemplateView):
    template_name = 'edit-account.html'

class CreateCoursePageView(TemplateView):
    template_name = 'create-course.html'

class AssignPageView(TemplateView):
    template_name = 'assign-people.html'


class NotificationsView(TemplateView):
    template_name = 'Notifications.html'

# Create your views here.
