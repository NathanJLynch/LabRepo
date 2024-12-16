

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.context_processors import request
from django.urls import reverse
from django.utils.timezone import now, timedelta
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
        email = request.POST.get('email')
        password = request.POST.get('password')
        # phone = request.POST.get('phone')
        role = request.POST.get('role_id')
        if name and email and password and role:
            try:
                # Create and save a new user
                User.objects.create(full_name=name, email=email, password=password, role_id=role)
            except IntegrityError:
                messages.error(request, 'Account already exists')
                return redirect('CreateAccount')
            # Redirect back to the accounts page
        return HttpResponseRedirect(reverse('ListAccounts'))

class EditAccountPageView(TemplateView):
    template_name = 'edit-account.html'


class coursesPageView(TemplateView):
    template_name = 'courses.html'

    def get_next_occurrences(self, days, start_date, occurrences=5):
        """
        Get the next `occurrences` dates for the specified days starting from `start_date`.
        """
        day_mapping = {
            "M": 0,
            "Tu": 1,
            "W": 2,
            "Th": 3,
            "F": 4,
            "Saturday": 5,
            "Sunday": 6,
        }
        days_of_week = [day_mapping[day] for day in days.split(", ") if day in day_mapping]
        upcoming_dates = []
        current_date = start_date

        while len(upcoming_dates) < occurrences:
            for day in sorted(days_of_week):
                diff = (day - current_date.weekday() + 7) % 7
                next_date = current_date + timedelta(days=diff)
                if next_date not in upcoming_dates:
                    upcoming_dates.append(next_date)
            current_date += timedelta(days=1)

        return sorted(upcoming_dates[:occurrences])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()

        # Fetch all courses from the database
        context['courses'] = Course.objects.all()
        courses = Course.objects.all()
        all_upcoming_events = []

        for course in courses:
            if course.days:
                upcoming_dates = self.get_next_occurrences(course.days, today, occurrences=5)
                for date in upcoming_dates:
                    all_upcoming_events.append({
                        "course_name": course.course_name,
                        "start_time": course.start_time,
                        "end_time": course.end_time,
                        "type": "Lecture",  # or course.type if it exists
                        "date": date,
                    })

        # Sort all events by date and take only the first 5
        all_upcoming_events = sorted(all_upcoming_events, key=lambda x: x["date"])[:5]
        context['upcoming_courses'] = all_upcoming_events
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
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        selected_days = request.POST.getlist('days')  # Get multiple values for 'days'
        days = ", ".join(selected_days)
        if course_name and course_code and course_sem and start_time and end_time  :
            # Create and save a new course
            Course.objects.create(
                course_name=course_name,
                course_code=course_code,
                course_sem= course_sem,
                course_instructor = course_instructor,
                start_time=start_time,
                end_time=end_time,
                days = days
            )
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