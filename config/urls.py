# Import Django's administration site.
from django.contrib import admin

# Import path for defining URLs.
# Import include so that we can connect the
# results application's URLs.
from django.urls import path, include
from results import views
from django.shortcuts import redirect

# Main URL configuration for the entire project.
urlpatterns = [

    path("", lambda request: redirect("student_login")),
    path("admin/", admin.site.urls),
    path("register/", views.student_register, name="student_register"),
    path("login/", views.student_login, name="student_login"),
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/score/<int:student_id>/", views.enter_score, name="enter_score"),
    path("logout/", views.student_logout, name="student_logout"),
    path("student/<int:student_id>/", views.student_result, name="student_result"),

    # Send requests to our results application.
    #
    # For example:
    # /student/1/
    #
    # will be handled by results/urls.py.
    path("", include("results.urls")),
]
