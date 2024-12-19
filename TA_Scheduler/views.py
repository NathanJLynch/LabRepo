

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.urls import reverse
from django.utils.timezone import now, timedelta
from django.views.generic import TemplateView
from TA_Scheduler.models import Course, UserList, User, Validator, CheckPermissions
import logging
import json
import re
from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    # Get the logged-in user
    user = request.user
    # Pass the user's full name and role to the template
    return render(request, 'dashboard.html', {
        'user_name': user.get_full_name() or user.username,  # This will fallback to the username if the full name is empty
        'role': user.role if hasattr(user, 'role') else 'Unknown Role'  # Ensure role is accessible
    })


from django.http import JsonResponse
from .models import User


def get_user(request):
    user_id = request.GET.get('id')
    if not user_id:
        return JsonResponse({"error": "User ID not provided"}, status=400)

    try:
        user = User.objects.get(id=user_id)
        data = {
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role_id,
            "skills": user.skills.split(",") if user.skills else []
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


class LoginPageView(TemplateView):
    template_name = 'LoginPage.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_full_name = request.POST.get('full_name', '').strip()
            user_password = request.POST.get('password', '').strip()

            # Check for admin credentials
            if user_full_name == 'admin' and user_password == 'password':
                return redirect('homePage')

            # Check for a valid user in the database
            try:
                user = User.objects.get(full_name=user_full_name)
                if user.password == user_password:
                    return redirect('homePage')
                else:
                    messages.error(request, 'Incorrect username or password')
            except User.DoesNotExist:
                messages.error(request, 'Incorrect username or password')

            return redirect('LoginPage')


class HomePageView(TemplateView):
    template_name = 'homePage.html'

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
                logger.info(f'User created: {User.full_name}')
            except IntegrityError:
                messages.error(request, 'Account already exists')
                return redirect('CreateAccount')
            # Redirect back to the accounts page
        return HttpResponseRedirect(reverse('ListAccounts'))


class CreateAccountPageView(TemplateView):
    template_name = 'create-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

    def get(self, request):
        """Render the Create Account form."""
        return render(request, 'create-account.html')

    def post(self, request):
        """Handle the form submission for creating a new account."""
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        role_id = request.POST.get('role_id', '').strip()  # Role (Supervisor, Instructor, TA)
        skills = request.POST.get('skills[]')  # Get the skills as a JSON string

        # Validation: Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('CreateAccount')

        # Validation: Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('CreateAccount')

        # Validation: Check if phone number format is valid using regex
        phone_regex = re.compile(r'^\d{3}-\d{3}-\d{4}$')  # Matches xxx-xxx-xxxx format
        if phone_number and not phone_regex.match(phone_number):
            messages.error(request, 'Please enter a valid phone number (xxx-xxx-xxxx).')
            return redirect('CreateAccount')

        # Validation: If role is TA, ensure at least one skill is provided
        skills_list = []
        if role_id == 'TA':
            try:
                skills_list = json.loads(skills)  # Parse JSON string into a Python list
            except json.JSONDecodeError:
                skills_list = []

            if not skills_list:
                messages.error(request, 'Teaching Assistants must have at least one skill.')
                return redirect('CreateAccount')

        # Adjust role saving logic: only supervisor should be saved as admin
        if role_id == 'supervisor':
            role_id = 'admin'  # Save supervisor as admin
        elif role_id == 'ta':
            role_id = 'TA'  # Ensure 'TA' is saved as 'TA'

        # Create the user
        user = User.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            role_id=role_id,  # Save role_id as "admin" for supervisor or "TA" for teaching assistants
            skills=skills_list if role_id == 'TA' else None,  # Save skills for TAs only
        )

        # Success message and redirect
        messages.success(request, 'Account created successfully.')
        return redirect('ListAccounts')

from django.shortcuts import get_object_or_404

class EditAccountPageView(TemplateView):
    template_name = 'edit-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.GET.get('id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            context['user_data'] = {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'role_id': user.role_id.lower(),
                'skills': user.skills if hasattr(user, 'skills') else []
            }
        return context

    def post(self, request):
        user_id = request.POST.get('user_id')
        if not user_id:
            messages.error(request, 'User ID is required.')
            return redirect('EditAccount')

        user = get_object_or_404(User, id=user_id)

        # Get form data
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_new_password = request.POST.get('confirm_new_password', '').strip()
        role_id = request.POST.get('role_id', '').strip()
        skills = request.POST.getlist('skills[]')

        # Validate required fields
        if not all([full_name, email, role_id]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect(f'EditAccount?id={user_id}')

        # Validate current password if changing password
        if new_password:
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect(f'EditAccount?id={user_id}')

            if new_password != confirm_new_password:
                messages.error(request, 'New passwords do not match.')
                return redirect(f'EditAccount?id={user_id}')

            user.set_password(new_password)

        # Update user fields
        user.full_name = full_name
        user.email = email
        user.phone_number = phone_number

        # Handle role and skills
        if role_id == 'supervisor':
            user.role_id = 'admin'
            user.skills = None
        elif role_id == 'ta':
            if not skills:
                messages.error(request, 'Teaching Assistants must have at least one skill.')
                return redirect(f'EditAccount?id={user_id}')
            user.role_id = role_id
            user.skills = skills
        else:
            user.role_id = role_id
            user.skills = None

        try:
            user.save()
            messages.success(request, 'Account updated successfully.')
            return redirect('ListAccounts')
        except Exception as e:
            messages.error(request, f'Error updating account: {str(e)}')
            return redirect(f'EditAccount?id={user_id}')



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
        #ensure user has permission
        CheckPermissions.check_create_delete_permissions(self, request.user)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        print(f"Found {users.count()} users in database")
        for user in users:
            print(f"User: {user.full_name}, Role: {user.role_id}")
        context['users'] = users
        return context

class sendNotificationView(TemplateView):
    template_name = 'sendNotification.html'

# Create your views here.