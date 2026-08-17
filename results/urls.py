# Import Django's path function.
# It allows us to define URLs for our application.
from django.urls import path

#Import the views from our results application.
from . import views

# These are the URLs belonging to the results application.
urlpatterns = [

    # Example URL:
    # http://127.0.0.1:8000/student/1/
    #
    # <int:student_id> captures the student's ID
    # and passes it to the student_result view.
    path(
        "student/<int:student_id>/",
        views.student_result,
        name="student_result"
    ),
]