from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.context_processors import request
from django.urls import reverse
from django.views.generic import TemplateView
from TA_Scheduler.models import Course, UserList, User, Validator


class LoginPageView(TemplateView):
    template_name = 'LoginPage.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_full_name = request.POST['full_name']
            user_password = request.POST['password']
            try:
                user = User.objects.get(full_name=user_full_name)
                if user.password == user_password:
                    return redirect('homePage')
                else:
                    messages.error(request, 'Incorrect username or password')
                    return redirect('LoginPage')
            except User.DoesNotExist:
                messages.error(request, 'Incorrect username or password')
                return redirect('LoginPage')


class HomePageView(TemplateView):
    template_name = 'homePage.html'


class CreateAccountPageView(TemplateView):
    template_name = 'create-account.html'



    def post(self, request, *args, **kwargs):
        # Get account details from the POST request
        name = request.POST.get('full-name')
        email = request.POST.get('course_code')
        password = request.POST.get('password')
        # phone = request.POST.get('phone')
        role = request.POST.get('role')

        User.objects.create(name=name, email=email, password=password, role_id=role)

        if name and email and password and role:
            # Create and save a new user
            User.objects.create(name=name, email=email, password=password, role_id=role)
        # Redirect back to the accounts page
        return HttpResponseRedirect(reverse('listAccounts'))

class EditAccountPageView(TemplateView):
    template_name = 'edit-account.html'


class coursesPageView(TemplateView):
    template_name = 'courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all courses from the database
        context['courses'] = Course.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # Handle course deletion
        delete_course_id = request.POST.get("delete_course_id")
        if delete_course_id:
            course = Course.objects.get(course_id=delete_course_id)
            course.delete()

        return redirect("courses")  # Redirect back to the same page
class CreateCoursePageView(TemplateView):
    template_name = 'create-course.html'

    def post(self, request, *args, **kwargs):
        # Get course details from the POST request
        course_name = request.POST.get('course_name')
        course_code= request.POST.get('course_code')
        course_sem = request.POST.get('course_sem')
        course_instructor = request.POST.get('course_instructor')
        if course_name and course_code and course_sem :
            # Create and save a new course
            Course.objects.create(course_name=course_name, course_code=course_code, course_sem= course_sem, course_instructor = course_instructor)
        # Redirect back to the courses page
        return HttpResponseRedirect(reverse('courses'))

class AssignPageView(TemplateView):
    template_name = 'assign-people.html'

class NotificationsView(TemplateView):
    template_name = 'Notifications.html'


class listAccountsView(TemplateView):
    template_name = 'listAccounts.html'

class sendNotificationView(TemplateView):
    template_name = 'sendNotification.html'

# Create your views here.