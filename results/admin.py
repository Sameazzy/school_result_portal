# Import Django's admin functionality
from django.contrib import admin

# Import the database models we created
from .models import (
    ClassRoom, 
    Student, 
    Subject, 
    AcademicSession, 
    Score
)

# Register these models with Django Admin.
# This allows the administrator to add, edit, and delete
# classes, students, subjects, and academic sessions.
admin.site.register(ClassRoom)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(AcademicSession)

# Register the Score model with a customized Admin interface.
# This allows us to control which information is displayed
# in the Scores list.
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):

    list_display = (
         "student",
        "subject",
        "academic_session",
        "ca_score",
        "exam_score",
        "display_total",
        "display_grade",
        "display_remark",
    )

# Display the automatically calculated total score.
    def display_total(self, obj):
        return obj.total

    # Change the column heading from "display_total" to "Total".
    display_total.short_description = "Total"

    # Display the automatically calculated grade.
    def display_grade(self, obj):
        return obj.grade

    # Change the column heading to "Grade".
    display_grade.short_description = "Grade"

    # Display the automatically calculated remark.
    def display_remark(self, obj):
        return obj.remark

    # Change the column heading to "Remark".
    display_remark.short_description = "Remark"