# Import Django's authentication functions.
from django.contrib.auth import authenticate, login, logout

# Import Django's User model for creating student login accounts.
from django.contrib.auth.models import User

# Import login_required to protect pages from unauthenticated users.
from django.contrib.auth.decorators import login_required

# Import transaction so User and Student are created together.
from django.db import transaction

# Import redirect for sending users to another page.
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

# Import our database models.
from .models import Student, Score, AcademicSession, ClassRoom

# Define Student Registration
def student_register(request):
    """
    Register a new student.

    Registration creates:
    1. A Django User account for login.
    2. A Student record for the school portal.

    The admission number is generated automatically
    by the Student model.
    """

    # Check if the registration form was submitted.
    if request.method == "POST":

        # Get information entered by the student.
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Get the selected class.
        classroom_id = request.POST.get("classroom")

        # Check that the passwords match.
        if password != confirm_password:

            return render(
                request,
                "results/register.html",
                {
                    "error": "Passwords do not match."
                }
            )

        # Check whether the username already exists.
        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "results/register.html",
                {
                    "error": "This username is already taken."
                }
            )

        # Check that a valid gender was selected.
        if gender not in ["M", "F"]:

            return render(
                request,
                "results/register.html",
                {
                    "error": "Please select a valid gender."
                }
            )

        # Check that a class was selected.
        if not classroom_id:

            return render(
                request,
                "results/register.html",
                {
                    "error": "Please select your class."
                }
            )

        try:

            # Create the User and Student together.
            with transaction.atomic():

                # Create the student's login account.
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                # Create the student's school record.
                #
                # The admission number will be generated
                # automatically by the Student model.
                student = Student.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    classroom_id=classroom_id
                )

            # Automatically log the student in.
            login(request, user)

            # Send the student to their dashboard.
            return redirect("student_dashboard")

        except Exception as e:

            # Display any error that occurs during registration.
            return render(
                request,
                "results/register.html",
                {
                    "error": str(e)
                }
            )

    # Get all available classes for the registration form.
    classrooms = ClassRoom.objects.all()

    # Display the registration page.
    return render(
        request,
        "results/register.html",
        {
            "classrooms": classrooms
        }
    )

#Define Login Functionality
def student_login(request):
    """
    Allow a student to log into the results portal.
    """

    # Check if the login form was submitted.
    if request.method == "POST":

        # Get the username and password entered by the student.
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check whether the username and password are valid.
        user = authenticate(
            request,
            username=username,
            password=password
        )

        # If the user is valid, log them in.
        if user is not None:

            login(request, user)

            # Send the student to their dashboard.
            return redirect("student_dashboard")

        # If login fails, show an error message.
        return render(
            request,
            "results/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    # Display the login page.
    return render(
        request,
        "results/login.html"
    )

#Create the Student Dashboard
@login_required
def student_dashboard(request):
    """
    Display the dashboard for the currently logged-in student.
    """

    # Find the student connected to the logged-in user.
    student = get_object_or_404(
        Student,
        user=request.user
    )

    # Display the student's dashboard.
    return render(
        request,
        "results/dashboard.html",
        {
            "student": student
        }
    )

#Logout View
@login_required
def student_logout(request):
    """
    Log the current student out of the portal.
    """

    # End the user's login session.
    logout(request)

    # Return the user to the login page.
    return redirect("student_login")
   
#Define Student Result
def student_result(request, student_id):
    """
    Display a student's result.

    The student can select an academic session and term.
    Only scores belonging to the selected session will
    be displayed.
    """

    # Retrieve the student using the ID from the URL.
    # If the student does not exist, Django returns a 404 error.
    student = get_object_or_404(
        Student,
        id=student_id
    )

    # Get all available academic sessions.
    # These will be used to create the session selection dropdown.
    academic_sessions = AcademicSession.objects.all()

    # Get the academic session ID from the URL query parameter.
    #
    # Example:
    # /student/1/?session=1
    selected_session_id = request.GET.get("session")

    # Start with an empty queryset.
    scores = Score.objects.none()

    # Default values for the result summary.
    total_score = 0
    average = 0

    # Store the selected academic session.
    selected_session = None

    # Only retrieve scores if the user selected a session.
    if selected_session_id:

        # Find the selected academic session.
        selected_session = get_object_or_404(
            AcademicSession,
            id=selected_session_id
        )

        # Retrieve only this student's scores
        # for the selected academic session.
        scores = Score.objects.filter(
            student=student,
            academic_session=selected_session
        ).select_related(
            "subject",
            "academic_session"
        )

        # Calculate the total score across all subjects.
        total_score = sum(
            score.total for score in scores
        )

        # Count the number of subjects.
        subject_count = scores.count()

        # Calculate the average.
        # Prevent division by zero if there are no scores.
        if subject_count > 0:
            average = total_score / subject_count

    # Send all required information to the template.
    return render(
        request,
        "results/student_result.html",
        {
            "student": student,
            "academic_sessions": academic_sessions,
            "selected_session": selected_session,
            "scores": scores,
            "total_score": total_score,
            "average": average,
        }
    )