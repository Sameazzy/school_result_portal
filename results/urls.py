# Import Django's path function.
from django.urls import path

# Import views from this application.
from . import views


urlpatterns = [
    # register a student.
    path(
        "register/",
        views.student_register,
        name="student_register"
    ),


    # Student login page.
    path(
        "login/",
        views.student_login,
        name="student_login"
    ),

    # Student dashboard.
    path(
        "dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    # Log the student out.
    path(
        "logout/",
        views.student_logout,
        name="student_logout"
    ),

    # Temporary direct student result URL.
    # We will replace this later with a protected
    # "My Result" page.
    path(
        "student/<int:student_id>/",
        views.student_result,
        name="student_result"
    ),
]