# Import Django's authentication functions.
from django.contrib.auth import authenticate, login, logout

# Import Django's User model for creating student login accounts.
from django.contrib.auth.models import User

# Import login_required to protect pages from unauthenticated users.
from django.contrib.auth.decorators import login_required

# Import transaction so User and Student are created together.
from django.db import transaction

from django.contrib import messages

# Import redirect for sending users to another page.
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

# Import our database models.
from .models import Student, Teacher, Score, AcademicSession, ClassRoom, Subject

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
    """Allow students and teachers to log into the portal."""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Log the user in.
            login(request, user)

            # Send teachers to the teacher dashboard.
            if Teacher.objects.filter(user=user).exists():
                return redirect("teacher_dashboard")

            # Send students to the student dashboard.
            if Student.objects.filter(user=user).exists():
                return redirect("student_dashboard")

            # User exists but has no Student or Teacher profile.
            logout(request)

            return render(
                request,
                "results/login.html",
                {
                    "error": "Your account is not linked to a student or teacher profile."
                }
            )

        return render(
            request,
            "results/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "results/login.html"
    )

#Create the Teacher Dashboard
@login_required
def teacher_dashboard(request):
    """Display students in the teacher's assigned classroom."""

    # Get the teacher linked to the logged-in user.
    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    # Get only students in the teacher's classroom.
    students = Student.objects.filter(
        classroom=teacher.classroom
    )

    return render(
        request,
        "results/teacher_dashboard.html",
        {
            "teacher": teacher,
            "students": students,
        }
    )

@login_required
def enter_score(request, student_id):
    """Allow a teacher to enter a score for a student in their class."""

    # Get the teacher linked to the logged-in user.
    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    # Get the selected student.
    student = get_object_or_404(
        Student,
        id=student_id,
        classroom=teacher.classroom
    )

    # Get available subjects and academic sessions.
    subjects = Subject.objects.all()
    academic_sessions = AcademicSession.objects.all()

    if request.method == "POST":

        subject_id = request.POST.get("subject")
        session_id = request.POST.get("academic_session")
        ca_score = request.POST.get("ca_score")
        exam_score = request.POST.get("exam_score")

        # Create or update the student's score.
        Score.objects.update_or_create(
            student=student,
            subject_id=subject_id,
            academic_session_id=session_id,
            defaults={
                "ca_score": ca_score,
                "exam_score": exam_score,
            }
        )

        messages.success(
            request,
            "Score saved successfully."
        )

        return redirect(
            "enter_score",
            student_id=student.id
        )

    return render(
        request,
        "results/enter_score.html",
        {
            "student": student,
            "subjects": subjects,
            "academic_sessions": academic_sessions,
        }
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
    # Find the teacher connected to the student's class
    teacher = Teacher.objects.filter(
        classroom=student.classroom
    ).first()

    # Display the student's dashboard.
    return render(
        request,
        "results/dashboard.html",
        {
            "student": student,
            "teacher": teacher,
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
    # Check if the logged-in user is a teacher.
    is_teacher = Teacher.objects.filter(
        user=request.user
    ).exists()
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
            "is_teacher": is_teacher,
        }
    )