

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.urls import reverse
from django.utils.timezone import now, timedelta,datetime
from django.views.generic import TemplateView
from TA_Scheduler.models import Course, UserList, User, Validator, CheckPermissions,Section
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
        phone = request.POST.get('phone')
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
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role_id = request.POST.get('role_id')  # Role (Supervisor, Instructor, TA)
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
        # phone_regex = re.compile(r'^\d{3}-\d{3}-\d{4}$')  # Matches xxx-xxx-xxxx format
        # if phone_number and not phone_regex.match(phone_number):
        #     messages.error(request, 'Please enter a valid phone number (xxx-xxx-xxxx).')
        #     return redirect('CreateAccount')

        # Validation: If role is TA, ensure at least one skill is provided
        skills_list = []
        if role_id.lower() == 'ta':
            try:
                skills_list = json.loads(skills) if skills else []
            except json.JSONDecodeError:
                skills_list = []

            if not skills_list:
                messages.error(request, 'Teaching Assistants must have at least one skill.')
                return redirect('CreateAccount')

        # Adjust role saving logic: Save appropriate role_id
        role_map = {
            'supervisor': 'admin',
            'instructor': 'instructor',
            'ta': 'TA',
        }
        role_id = role_map.get(role_id.lower(), None)

        # Create the user
        user = User.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            password=password,
            role_id=role_id,  # Save role_id as "admin" for supervisor or "TA" for teaching assistants
            skills=skills_list if role_id == 'ta' else None,  # Save skills for TAs only
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



class CreateSection(TemplateView):
    template_name = 'create-section.html'

    def get_context_data(self, **kwargs):
        # Retrieve the course based on course_id from query parameters
        course_id = self.request.GET.get('course_id')

       # Ensure the course exists
        course = Course.objects.get(course_id=course_id)

        # Fetch sections for the course
        sections = Section.objects.filter(course=course)

        # Add data to context
        context = super().get_context_data(**kwargs)
        context.update({
            'course': course,
            'sections': sections,
        })
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_section_id' in request.POST:
            # Handle section deletion
            delete_section_id = request.POST.get('delete_section_id')

            # Ensure the section exists
            section = Section.objects.get(id=delete_section_id)

            # Delete the section
            section.delete()

            # Redirect back to the same page with the course context
            course_id = request.GET.get('course_id')
            return redirect(f'/create-section/?course_id={course_id}')
        else:
            course_id = request.POST.get('course_id')

            # Ensure the course exists
            course = Course.objects.get(course_id=course_id)

            # Handle form submission
            number = request.POST.get('number')
            section_type = request.POST.get('type')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            days = request.POST.getlist('days')  # List of selected days
            ta = request.POST.get('ta')
            instructor = request.POST.get('instructor')

            # Save the new section
            Section.objects.create(
                course=course,
                number=number,
                type=section_type,
                start_time=start_time,
                end_time=end_time,
                days=",".join(days),  # Save as comma-separated values
                ta=ta,
                instructor=instructor,
            )

            # Redirect back to courses
            return redirect(f'/create-section/?course_id={course_id}')

class coursesPageView(TemplateView):
    template_name = 'courses.html'

    def get_next_occurrences(self, days, start_date,course_sem, occurrences=5):
        day_mapping = {
            "M": 0,
            "Tu": 1,
            "W": 2,
            "Th": 3,
            "F": 4,
            "Saturday": 5,
            "Sunday": 6,
        }
        days_of_week = [day_mapping[day] for day in days.split(",") if day in day_mapping]
        upcoming_dates = []
        current_date = start_date

        # Map semester to month ranges
        semester_mapping = {
            "spring": (1, 5),  # January to May
            "summer": (6, 8),  # June to August
            "fall": (9, 12),  # September to December
        }

        # Parse course_sem (e.g., "spring-2025") to validate it
        try:
            sem_name, sem_year = course_sem.split("-")
            sem_year = int(sem_year)
            if sem_name.lower() in semester_mapping:
                sem_start_month, sem_end_month = semester_mapping[sem_name.lower()]
                sem_start_date = datetime(sem_year, sem_start_month, 1).date()
                sem_end_date = datetime(sem_year, sem_end_month, 1).date() + timedelta(days=31)
            else:
                return []  # Invalid semester format
        except ValueError:
            return []  # Invalid semester format

        # Ensure current date is within the course semester
        if not (sem_start_date <= current_date <= sem_end_date):
            return []  # Not an upcoming course for the current date

        # Generate upcoming dates
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

        courses = Course.objects.all()

        # Fetch all sections from the database
        sections = Section.objects.all()
        all_upcoming_sections = []

        for section in sections:
            if section.days:
                upcoming_dates = self.get_next_occurrences(section.days, today,section.course.course_sem, occurrences=5)
                for date in upcoming_dates:
                    all_upcoming_sections.append({
                        "course_name": section.course_name,
                        "number": section.number,
                        "type": section.type,
                        "start_time": section.start_time,
                        "end_time": section.end_time,
                        "date": date,
                        "days": section.days,
                        "ta": section.ta,
                        "instructor": section.instructor,
                    })

        # Sort all sections by date and time, and take only the first 5
        sorted_upcoming_sections = sorted(all_upcoming_sections, key=lambda x: x["date"])[:5]

        # Add data to the context
        context['upcoming_sections'] = sorted_upcoming_sections
        context['courses'] = Course.objects.all()  # Optional: Fetch all courses if needed elsewhere
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
        # CheckPermissions.check_create_delete_permissions(self, request.user)
        # Get course details from the POST request
        course_name = request.POST.get('course_name')
        course_code= request.POST.get('course_code')
        course_sem = request.POST.get('course_sem')

        if course_name and course_code and course_sem  :
            # Create and save a new course
            Course.objects.create(
                course_name=course_name,
                course_code=course_code,
                course_sem= course_sem,
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