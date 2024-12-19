"""
URL configuration for InB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from TA_Scheduler.views import LoginPageView
from TA_Scheduler.views import HomePageView
from TA_Scheduler.views import coursesPageView
from TA_Scheduler.views import CreateAccountPageView
from TA_Scheduler.views import EditAccountPageView
from TA_Scheduler.views import CreateCoursePageView, AssignPageView,NotificationsView,listAccountsView,sendNotificationView,CreateSection

urlpatterns = [
    path('', LoginPageView.as_view(), name='LoginPage'),

    path('LoginPage', LoginPageView.as_view(), name='LoginPage'),
    path('homePage', HomePageView.as_view(), name='homePage'),
    path('Courses', coursesPageView.as_view(), name='courses'),
    path('create-section/', CreateSection.as_view(), name='create_section'),
    path('CreateAccount', CreateAccountPageView.as_view(), name='CreateAccount'),
    path('EditAccount', EditAccountPageView.as_view(), name='EditAccount'),
    path('CreateCourse', CreateCoursePageView.as_view(), name='CreateCourse'),
    path('Assign', AssignPageView.as_view(), name='Assign'),
    path('Notifications', NotificationsView.as_view(), name='Notifications'),
    path('ListAccounts', listAccountsView.as_view(), name='ListAccounts'),
    path('sendNotification', sendNotificationView.as_view(), name='sendNotification'),

    path('admin/', admin.site.urls),
]
