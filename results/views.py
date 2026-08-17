# render() is used to display an HTML page.
# get_object_or_404() finds an object or returns
# a 404 error if the object doesn't exist.
from django.shortcuts import render, get_object_or_404

# Create your views here.
# Import the models we need.
from .models import Student, Score

def student_result(request, student_id):
    """
    Display the academic result for a particular student.

    The student ID comes from the URL.

    Example:
        /student/1/

    means:
        student_id = 1
    """

    # Find the student whose ID was provided in the URL.
    #
    # If the student doesn't exist, Django automatically
    # displays a "Page Not Found" response.

    student = get_object_or_404(
        Student,
        id=student_id
    )
    # Retrieve all scores belonging to this student.
    #
    # select_related() tells Django to retrieve the related
    # subject and academic session information efficiently.
    scores = Score.objects.filter(
        student=student
    ).select_related(
        "subject",
        "academic_session"
    )
    #sum all totals
    total_score = sum(
        score.total for score in scores
    )
    # Count the number of subjects.
    subject_count = len(scores)

    # Calculate the student's average.
    #
    # The condition prevents division by zero if
    # the student has no scores.
    average = (
        total_score / subject_count
        if subject_count
        else 0
    )

    # Send all this information to our HTML template.
    return render(
        request,
        "results/student_result.html",
        {
            "student": student,
            "scores": scores,
            "total_score": total_score,
            "average": average,
        }
    )